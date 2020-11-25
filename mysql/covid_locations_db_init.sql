CREATE TABLE Cases(
    address_visited VARCHAR(100) NOT NULL,
    netid VARCHAR(255) NOT NULL,
    timestamp DATETIME,
    block_id VARCHAR(255),
    PRIMARY KEY(netid, address_visited)
);
CREATE TABLE Addresses(
    _address VARCHAR(255) NOT NULL,
    block_id VARCHAR(255),
    num_cases INT,
    PRIMARY KEY(_address)
);
CREATE TABLE Blocks(
    block_id VARCHAR(255) NOT NULL,
    num_cases_blk INT,
    PRIMARY KEY(block_id)
);
