// SPDX-License-Identifier: MIT
pragma solidity ^ 0.8.3;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Context.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";


/**
 * @title SimpleToken
 * @dev Very simple ERC20 Token example, where all tokens are pre-assigned to the creator.
 * Note they can later distribute these tokens as they wish using `transfer` and other
 * `ERC20` functions.
 */
 
 
 //防止尚未建立的版或文章被新增字串
 
contract NccuToken is Context, ERC20 {
    
    function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
        if (_i == 0) {
            return "0";
        }
        uint j = _i;
        uint len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len;
        while (_i != 0) {
            k = k-1;
            uint8 temp = (48 + uint8(_i - _i / 10 * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            _i /= 10;
        }
        return string(bstr);
    }
    
    //版面
    string[] private _comunity;
    
    //誰有甚麼版面
    mapping(string => address) private _comunityOwner;
    
    //版面有甚麼文章
    mapping(string => string[]) private _articleTitle;
    
    //誰擁有這個文章
    mapping(string => mapping(string => address)) private _articleOwner;
    
    //誰擁有進入這個文章的許可
    mapping(string => mapping(string => mapping(address => bool))) private _articleLicense;
    
    //這個版面的文章有甚麼內容
    mapping(string => mapping(string => string[])) private _article;
    
    //這個版面文章的花費
    mapping(string => mapping(string => uint256)) private _articleCost;
    
    //這個版面的文章有甚麼留言
    mapping(string => mapping(string => string[])) private _replyMessage;
    
    //誰有這個留言
    mapping(string => mapping(string => mapping(string => address))) private _replyMessageOwner;
    
    constructor () public ERC20("NccuToken", "NCCU") {
        _mint(_msgSender(), 100000000 * (10 ** uint256(decimals())));
        _comunity.push("def");
    }
    
    string private _temp;
    
    function createComunity(string memory comunity_) public{
        //標上編號以及合併字串
        comunity_ = string(abi.encodePacked(string(abi.encodePacked(uint2str(_comunity.length), " ")), comunity_));
        
        _comunity.push(comunity_);
        
        _comunityOwner[comunity_] = _msgSender();
        
        _burn(msg.sender, 10000 * (10 ** uint256(decimals())));
    }
    
    function createArticle(string memory comunity_, string memory articleTitle_, string memory article_) public {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        
        //標上編號以及合併字串
        articleTitle_ = string(abi.encodePacked(string(abi.encodePacked(uint2str(_articleTitle[comunity_].length + 1), " ")), articleTitle_));
        
        _articleTitle[comunity_].push(articleTitle_);
        
        _article[comunity_][articleTitle_].push(article_);
        
        _articleCost[comunity_][articleTitle_] = 0;
        
        _articleOwner[comunity_][articleTitle_] = _msgSender();
        
        _mint(msg.sender, 10 * (10 ** uint256(decimals())));
    }
    
    function createArticleCost(string memory comunity_, string memory articleTitle_, uint256 cost_) public {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        _have = true;
                    }
                }
            }
        }
        require(_have == true,  "don't have articleTitle");
        
        
        _articleCost[comunity_][articleTitle_] = cost_;
    }
    
    function createReplyMessage(string memory comunity_, string memory articleTitle_, string memory replyMessage_) public {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        _have = true;
                    }
                }
            }
        }
        require(_have == true,  "don't have articleTitle");
        
        //標上編號以及合併字串
        replyMessage_ = string(abi.encodePacked(string(abi.encodePacked(uint2str(_replyMessage[comunity_][articleTitle_].length + 1), " ")), replyMessage_));
        
        _replyMessage[comunity_][articleTitle_].push(replyMessage_);
        
        _replyMessageOwner[comunity_][articleTitle_][replyMessage_] = _msgSender();
        
        _mint(msg.sender, 1 * (10 ** uint256(decimals())));
    }
    
    function getComunity() public view returns(string[] memory) {
        return _comunity;
    }
    
    function getArticleTitle(string memory comunity_) public view returns(string[] memory) {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        
        return _articleTitle[comunity_];
    }
    
    function payArticle(string memory comunity_, string memory articleTitle_) public{
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        _have = true;
                    }
                }
            }
        }
        require(_have == true,  "don't have articleTitle");
        
        _burn(msg.sender,  _articleCost[comunity_][articleTitle_] * (10 ** uint256(decimals())));
        _articleLicense[comunity_][articleTitle_][_msgSender()] = true;
        
    }
    
    function getArticle(string memory comunity_, string memory articleTitle_, address address_) public view returns(string[] memory) {
        if(_articleCost[comunity_][articleTitle_]>0){
            require(_articleLicense[comunity_][articleTitle_][address_] == true,  "don't have articleLicense");
        }

        return _article[comunity_][articleTitle_];
    }
    
    function getArticleCost(string memory comunity_, string memory articleTitle_) public view returns(uint256) {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        _have = true;
                    }
                }
            }
        }
        require(_have == true,  "don't have articleTitle");
        
        return _articleCost[comunity_][articleTitle_];
    }
    
    function getReplyMessage(string memory comunity_, string memory articleTitle_) public view returns(string[] memory) {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        _have = true;
                    }
                }
            }
        }
        require(_have == true,  "don't have articleTitle");
        
        return _replyMessage[comunity_][articleTitle_];
    }
    
    function getComunityOwner(string memory comunity_) public view returns(address) {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        
        return _comunityOwner[comunity_];
    }
    
    function getArticleOwner(string memory comunity_, string memory articleTitle_) public view returns(address) {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        _have = true;
                    }
                }
            }
        }
        require(_have == true,  "don't have articleTitle");
        
        return _articleOwner[comunity_][articleTitle_];
    }
    
    function getArticleLicense(string memory comunity_, string memory articleTitle_, address address_) public view returns(bool) {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        _have = true;
                    }
                }
            }
        }
        require(_have == true,  "don't have articleTitle");
        
        return _articleLicense[comunity_][articleTitle_][address_];
    }
    
    function getReplyMessageOwner(string memory comunity_, string memory articleTitle_, string memory replyMessage_) public view returns(address) {
        bool _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
             if((keccak256(abi.encodePacked(_comunity[_i])))==(keccak256(abi.encodePacked(comunity_)))){
                 _have = true;
             }
        }
        require(_have == true,  "don't have comunity");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        _have = true;
                    }
                }
            }
        }
        require(_have == true,  "don't have articleTitle");
        _have = false;
        for(uint _i = 0; _i < _comunity.length; _i++){
            if(keccak256(abi.encodePacked(_comunity[_i])) == keccak256(abi.encodePacked(comunity_))){
                for(uint _j = 0; _j < _articleTitle[_comunity[_i]].length; _j++){
                    if(keccak256(abi.encodePacked(_articleTitle[_comunity[_i]][_j])) == keccak256(abi.encodePacked(articleTitle_))){
                        for(uint _k = 0; _k < _replyMessage[_comunity[_i]][_articleTitle[_comunity[_i]][_j]].length; _k++){
                            if(keccak256(abi.encodePacked(_replyMessage[_comunity[_i]][_articleTitle[_comunity[_i]][_j]][_k])) == keccak256(abi.encodePacked(replyMessage_))){
                                _have = true;
                            }
                        }
                    }
                }
            }
        }
        require(_have == true,  "don't have replyMessage");
        
        return _replyMessageOwner[comunity_][articleTitle_][replyMessage_];
    }
}