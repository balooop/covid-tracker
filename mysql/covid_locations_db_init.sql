CREATE TABLE Cases(
    address_visited char(100) NOT NULL,
    case_id VARCHAR(255) NOT NULL,
    timestamp DATETIME,
    PRIMARY KEY(case_id, address_visited)
);
CREATE TABLE Addresses(
    _address VARCHAR(255) NOT NULL,
    block_id VARCHAR(255),
    num_cases INT,
    PRIMARY KEY(_address)
);
CREATE TABLE Blocks(
    block_id INT NOT NULL,
    num_cases_blk INT,
    PRIMARY KEY(block_id)
);
