// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.12;

import "./console.sol";

contract D {
    uint256 public x;

    constructor(uint256 a) payable {
        x = a;
        console.log(
            "D.constructor(), a=%d, value=%d, msg.sender=%s",
            a,
            msg.value,
            msg.sender
        );
    }
}

contract C {
    D d = new D(4); // will be executed as part of C's constructor

    constructor() payable {
        console.log(
            "C.constructor(), value=%d, msg.sender=%s",
            msg.value,
            msg.sender
        );
    }

    function createD(uint256 arg) public {
        D newD = new D(arg);
        console.log("x=%d", newD.x());
    }

    function createAndEndowD(uint256 arg, uint256 amount) public payable {
        // Send ether along with the creation
        D newD = new D{value: amount}(arg);
        console.log("x=%d", newD.x());
    }

    function createDSalted(bytes32 salt, uint256 arg) public {
        // This complicated expression just tells you how the address
        // can be pre-computed. It is just there for illustration.
        // You actually only need ``new D{salt: salt}(arg)``.
        address predictedAddress = address(
            uint160(
                uint256(
                    keccak256(
                        abi.encodePacked(
                            bytes1(0xff),
                            address(this),
                            salt,
                            keccak256(
                                abi.encodePacked(type(D).creationCode, arg)
                            )
                        )
                    )
                )
            )
        );
        D d = new D{salt: salt}(arg);
        console.log(
            "C.createDSalted() created a new D contract at address %s",
            predictedAddress
        );
        require(address(d) == predictedAddress);
    }

    receive() external payable {
        console.log("C.receive(), receiving %d ether", msg.value);
    }
}
