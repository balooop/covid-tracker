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
            SET num_cases = (   SELECT count(*)
                                FROM   Cases c
                                WHERE  c._address = new.address_visited
                            )
            WHERE _address = new.address_visited;
        END IF;


        #### CREATE/UPDATE BLOCK TABLE ####
        SET @block =  ( SELECT block_id
                        FROM Blocks
                        WHERE new.block_id = block_id);
        # if block doesn't exist, insert into there
        IF @block IS NULL THEN
            INSERT INTO Blocks(block_id, num_cases_blk)
                        VALUES(new.block_id, 1);
        # if block does exist, update number of cases per block
        ELSE
            UPDATE Blocks
            SET num_cases_blk = (SELECT count(num_cases)
                                FROM Addresses
                                GROUP BY block_id)
            WHERE block_id = new.block_id;

        END IF;

    END;
    $$
    DELIMITER ;
