CREATE TRIGGER InsertAddress
    AFTER INSERT ON Cases
    for each row
    begin
        SET @count = (  SELECT _address 
                        FROM Addresses 
                        WHERE _address = new._address);
        # insert case: if the address isn't present, we insert
        IF @count IS NULL THEN 
            INSERT INTO Addresses(_address, block_id, num_cases) 
                        VALUES(new._address, new.block_id, 1);
            # add to Blocks table
        # update case: if the address is present, we update the num_cases
        ELSE
            UPDATE Addresses
            SET num_cases = num_cases + 1
            WHERE _address = new._address
        END IF;

    END;

