import requests
import json



def main():
    confernce_api_url = "https://o136z8hk40.execute-api.us-east-1.amazonaws.com/dev/get-list-of-conferences"
    response = requests.get( confernce_api_url) #Reading the data from the url
    json_response=response.json()
#    print("data")
    free_conferences, paid_conferences = json_response['free'], json_response['paid']
    all_conferences = free_conferences + paid_conferences #joining two list of data
#    data=json.dumps(all_conferences,indent=4,separators=(". ", " = "))
#   print(data)

    duplicates_filtered_conferences = remove_exact_duplicates(all_conferences)#filtering the duplicates
    display_conferences(duplicates_filtered_conferences) #displaying the identified duplicates
    unique_conferences = remove_semantic_duplicates(duplicates_filtered_conferences)#removing the semantic duplicate
    display_conferences(unique_conferences)#diplayingg the   identified semantic duplicate


def remove_exact_duplicates(conferences):
    conference_dict = {}
    for conference in conferences:
        conf_name = conference['confName']
        if not conf_name in conference_dict:#unquie name
            conference_dict[conf_name] = conference
    return conference_dict


def remove_semantic_duplicates(conferences):
    conference_dict = {}
    for conf_name in conferences:
        conference = conferences[conf_name]
        semantic_conf_key = conference['confUrl'].strip() + "|" + conference['confStartDate'].strip() + "|" + \
                            conference['confEndDate'].strip()
        if not semantic_conf_key in conference_dict:#using all three attributes to find semantic
            conference_dict[semantic_conf_key] = conference
      #  else:
    #    print("duplicate: semantic_conf_key:{}\n" .format(semantic_conf_key))
    return conference_dict


def display_conferences(conferences):
    print("name,date,venue,entry_type,url,registration_url")
    for conf_name in conferences:
        conference = conferences[conf_name]
        print("{},{},{},{},{},{}".format(
            conference["confName"], conference["confStartDate"], conference["venue"], conference["entryType"],
            conference["confUrl"], conference["confRegUrl"]))


if __name__ == "__main__":
    main()
