# Application model
## Tweets attributes
### Creation timestamp
The attribute `created_at` indicates the moment, in UTC time, when the tweet was created. This attribute will be very
useful as old tweets will not have any value for the streaming analysis.
  
### Text
In the attribute `text` is where the content of the tweet resides. There are three possibilities:

- **Is an original tweet:** When the tweet is a new status from the user.
- **Is an answer to a tweet:** When the user answer another tweet and initiates a conversation.
- **Is a retweet:** When the user retweet another user tweet.

Depending of the case, the interesting information can be found in different parts of the object received by the API.

#### Original tweet
When the tweet is an original one from an user, this is that it is new and not related to other tweet the content in
the attribute `text` will be processed.

#### Response tweet
When the tweet is a response to another tweet, the value information is both the content of the response and the tweet
that is answered. There will be some times where the original tweet has been already examined, because it is highly 
probable that it contains related content but, in other cases, the original tweet could be useful.

The original tweet is available in `quoted_status`. In this case, the content of the original tweet will be 
concatenated to the answer and the two tweets will be processed. 

#### Retweet
When the tweet is a retweet from another user, the `text` attribute starts with `RT @user` where the user is the
username of the user who post the original tweet. 

In this case, the valuable information is contained in the original
tweet, the content of this tweet is available in the attribute `retweeted_status` and it will be used in the same way
as on original tweet.

### Location
In some cases, the tweet contains information about the location where the it was written. This could be very useful to
discard some tweets directly when it is written outside Spain or Madrid. The object that contains that information
is contained in the attribute called `place`. 

Inside the location object could be found some useful attributes like:

- `place_type`: The type of location represented by this place. Interesting when the value is city.
- `name`: Short human-readable representation of the place’s name.
- `country_code`: Shortened country code representing the country containing this place.
- `country`: Name of the country containing this place. 

More specific information can be found in
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/geo-objects

### User
The information about the user that post the tweets also comes with the received data. It forms an user object that
contains all the profile information about it, it is under the attribute `user`. The information that can be useful
about this is the attribute `id` that will allow us to identify an specific user.

More specific information can be found in
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
