DELIMITER $$
CREATE TRIGGER InsertAddressfromCases
    AFTER INSERT ON Cases
    for each row
    begin
        SET @count = (  SELECT _address 
                        FROM Addresses 
                        WHERE _address = new.address_visited);
        IF @count IS NULL THEN 
            INSERT INTO Addresses(_address, block_id, num_cases) 
                        VALUES(new.address_visited, new.block_id, 1);
        ELSE
            UPDATE Addresses
            SET num_cases = num_cases + 1
            WHERE _address = new.address_visited;
        END IF;

    END;
    $$
    DELIMITER ;
