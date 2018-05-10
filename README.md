# Auction API
---
### Use any client to consume the API(Postman, curl preferred)

**Note** I have used Flask API. Flask API is an implementation of the same web browsable APIs that Django REST framework provides.

## Usage

1) To list all items on auction-

  * `13.232.64.101/items/all` method= **GET**

2) To list upcoming auctions-
  * `13.232.64.101/items/upcoming` method= **GET**
  
3) To list previous auctions-
 
  * `13.232.64.101/items/previous` method= **GET**

4) To list details on an item-

  * `13.232.64.101/item/<item_id>` method= **GET**, item_id = 1,2,3,4,...
 
5) To register user-
  
  *  `13.232.64.101/auth/register` method= **POST**, In request body(form.data) --> email, password
 
6) To login user-

  * `13.232.64.101/auth/login` method= **POST**, In request body(form.data) --> email, password

**Note** For auth, token-based auth is used. You'll receive a token in response to login request. Since only logged in users can place bids, copy that token and send it via 'Authorization' request header while making request to place bets. Token expires every 10 minutes so login again to generate new token if you get an Expired token response. Shown below.

You can also use these credentials-

email = 'a@a.com'

password = 'a'

7) To place bids-(You must have the auth token which you got in response after successful login)

  * `13.232.64.101/item/bid` method= **POST**,
  
  In request body(form.data) --> bid_on_item(Item ID on which to bid like 1,2,3,4,..), bid_amount(Amount to bid. Any float value)
  In request header --> `'Authorization': 'Bearer <token>'`  (Don't forget the space between Bearer and token)
 
8) To view all bids placed by a user-
  * `13.232.64.101/bids/user/<user_id>` method= **GET**, user_id = 1,2,3,4,...
  
## Database tables
Find tables and schema in screenshots/ directory
