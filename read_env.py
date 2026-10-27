import os

env_var_not_found = "<eol type='sark'>END OF LINE, PROGRAM</eol>"

api_key = os.getenv("OMLX_API_KEY", env_var_not_found)

if (api_key == env_var_not_found):
    print("DENIED INTELLIGENCE AUGMENTATION")
else:
    print(f"{api_key =}")
