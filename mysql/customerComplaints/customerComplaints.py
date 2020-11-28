import pymongo


client = pymongo.MongoClient("mongodb+srv://user:cs411project@cluster0.2xbcj.mongodb.net/?retryWrites=true&w=majority")
db = client[ "Complaints" ]
col = db[ "Complaints" ] 


    
def handler(event, context):
  
  maskFlag = 0
  socialDistancingFlag = 0
  sickFlag = 0
  dirtyFlag = 0
  
  maskWords = ['not wearing', 'covering', 'wearing', 'not wearing', 'no mask', 'no masks', 'masks under nose', 'without masks', 'took off mask', 'without mask', 'took off masks', 'mask under nose']
  socialDistancing = ['too many people', 'social distancing', 'close', 'group', 'groups', 'crowd',  'crowds', 'crowded', 'no space', '6 feet', 'close', 'touching', 'shaking hands', 'sharing food']
  sick = ['cough', 'coughing', 'sick', 'ill', 'sneeze', 'sneezing', 'drinking the liquids on the floor of kams', 'sneezed', 'puke', 'debilitated', 'infected', 'green', 'ailing', 'frail', 'fever', 'feverish']
  dirty = ['dirty', 'nasty', 'gross', 'not clean', 'nav', 'unsanitary', 'unclean', 'not sanitary', 'grubby', 'filthy', 'unwashed', 'not washed', 'stains', 'stain', 'smeared']
  
  cmpl = event['Complaints']
  addr = event['Address']

  for word in maskWords:
      if word in cmpl:
          maskFlag = 1
          break
  for word in socialDistancing:
      if word in cmpl:
          socialDistancingFlag = 1
          break
  for word in sick:
      if word in cmpl:
          sickFlag = 1
          break
  for word in dirty:
      if word in cmpl:
          dirtyFlag = 1
          break
    
  personDocument = {
    "Address": addr,
    "violations": [cmpl],
    "mask": maskFlag,
    "socialDistancing": socialDistancingFlag,
    "sick": sickFlag,
    "dirty": dirtyFlag
  }
  if(col.find({'Address': addr}).count() > 0):
    myquery = { "Address": addr }
    curViol = col.find({'Address': addr})
    violList = [cmpl]
    numMask = 0
    numSocialDist = 0
    numSick = 0
    numDirty = 0
    for x in curViol:
      numMask = x["mask"]
      numSocialDist = x["socialDistancing"]
      numSick = x["sick"]
      numDirty = x["dirty"]
      if(isinstance(x["violations"], str)):
        violList.append(x["violations"])
      else:
        for violation in x["violations"]:
          violList.append(violation)
    newvalues = { "$set": { "violations": violList, "mask": numMask + maskFlag, "socialDistancing": numSocialDist + socialDistancingFlag, "sick": numSick + sickFlag, "dirty": numDirty + dirtyFlag} }
    col.update_one(myquery, newvalues)
  else:
    col.insert_one(personDocument)

  client.close()
  return