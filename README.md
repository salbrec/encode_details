# encode_details
Scripts for extracting detail information about ENCODE datasets

The parser function are within the ./json_parser/main_parser.py script. Basically, one can simply import this script in order to apply the functions. 

There is not that much to say. The example_main.py collects the biosample information for sme random ChIP-seq accessions. From that script one can get an idea for how to use.

Important to know is that even though 2 replicates often come from the same cell line growth, they might be considered as different biosmples as they were finally prepared on two different days. In such cases ENCODE indeed considers them as two different biosamples with two different IDs. And it's the biosample that keeps the information about sex and age. However, there is consistency as the two biosamples do have the same donor in such cases which abloutely makes sense. The implementation here cares about all these cases and it should work.


