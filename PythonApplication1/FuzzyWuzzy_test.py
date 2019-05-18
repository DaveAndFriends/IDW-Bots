from fuzzywuzzy import process
from fuzzywuzzy import fuzz
Str1 = "submission statement"
Str4Compare = ["SuBmIsSiOn StAtEmEnT","sub stmt","subssion stament","[submission statement]:","submissionstatement"]

for cmpStr in Str4Compare:
    Ratio = fuzz.ratio(Str1.lower(),cmpStr.lower())
    #Partial_Ratio = fuzz.partial_ratio(Str1.lower(),cmpStr.lower())
    Token_Sort_Ratio = fuzz.token_sort_ratio(Str1,cmpStr)
    #Token_Set_Ratio = fuzz.token_set_ratio(Str1,cmpStr)

    print(Str1 + " vs " + cmpStr)
    print(Ratio)
    #print(Partial_Ratio)
    print(Token_Sort_Ratio)
    #print(Token_Set_Ratio)
    print("----------------")

reply_cmt = "This post was removed because it appears to be missing a submission statement.\n\n"
+"Submission statements are required\n\n"
+"* on all non-text posts\n"
+"* to be a top-level comment from OP\n"
+'* to start with the text "Submission statement"\n'
+'* to be at least 70 characters in length (excluding "Submission statement")\n'
+'* to be posted within 20 minutes of post creation\n\n'
+'Once you have posted your submission statement, it will be approved by the moderators.\n\n'
+'*I am a bot, and this action was performed automatically. Please* [*contact the moderators of this subreddit*](https://www.reddit.com/message/compose/?to=/r/IntellectualDarkWeb) *if you have any questions or concerns.*'