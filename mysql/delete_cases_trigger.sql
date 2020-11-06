DELIMITER $$
CREATE TRIGGER DeleteCase
    BEFORE DELETE ON Cases
    for each row
    begin
        # find all cases with the netid in cases
        # for each address visited by that netid
        # decrement in block and addresses
        set @block =  ( SELECT block_id
                        FROM Addresses a
                        WHERE a._address = old.address_visited);

        UPDATE Addresses
        SET num_cases = num_cases - 1
        WHERE _address = old.address_visited;
        
        UPDATE Blocks
        SET num_cases_blk = num_cases_blk - 1
        WHERE block_id = @block;

    END;
    $$
DELIMITER ; 



/* 
DEFINITELY WORKING
DELIMITER $$
CREATE TRIGGER InsertAddressfromCases
    AFTER INSERT ON Cases
    for each row
    begin
        #### CREATE/UPDATE ADDRESSES TABLE ####
        # checks if address is in Addresses table via select
        SET @count = (  SELECT _address 
                        FROM Addresses 
                        WHERE _address = new.address_visited);
        # if address not in Addresses table, insert the address
        IF @count IS NULL THEN 
            INSERT INTO Addresses(_address, block_id, num_cases) 
                        VALUES(new.address_visited, new.block_id, 1);
        # else, just update number of cases
        ELSE
            UPDATE Addresses
            SET num_cases = num_cases + 1
            WHERE _address = new.address_visited;
        END IF; */