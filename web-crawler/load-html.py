#!/usr/bin/python3

from io import StringIO
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Function to remove tags
def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
 
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

url_list = [
    "https://developer.cyberark.com/blog/a-poisoned-pipeline-understanding-cyberattacks-in-the-build-process/",
    "https://developer.cyberark.com/blog/honeypots-and-honeytokens-trapping-attackers-with-source-code-lures/",
    "https://developer.cyberark.com/blog/what-is-slsa-supply-chain-levels-for-software-artifacts/",
    "https://developer.cyberark.com/blog/chatgpt-is-here-how-to-use-ai-to-write-code-and-best-practices-for-security/",
    "https://developer.cyberark.com/blog/kubecon-2023-identity-security-a-whole-new-world/",
    "https://developer.cyberark.com/blog/security-best-practices-for-cloud-native-development-a-review-of-cloud-native-computing-foundation-resources/",
    "https://developer.cyberark.com/blog/the-sword-in-the-darkness-the-watcher-on-the-wall/",
    "https://developer.cyberark.com/blog/secure-ci-cd-pipelines-best-practices-for-managing-ci-cd-secrets/",
    "https://developer.cyberark.com/blog/kubernetes-security-best-practices-for-kubernetes-secrets-management/",
    "https://developer.cyberark.com/blog/environment-variables-dont-keep-secrets-best-practices-for-plugging-application-credential-leaks/",
    "https://developer.cyberark.com/blog/installing-conjur-in-an-eks-kubernetes-cluster-with-helm/",
    "https://developer.cyberark.com/blog/using-conjur-secrets-in-containerized-ansible-tower-applications/",
    "https://developer.cyberark.com/blog/technical-deep-dive-using-conjur-secrets-in-vm-deployed-ansible-tower-applications/",
    "https://developer.cyberark.com/blog/technical-deep-dive-security-automation-with-red-hat-ansible-tower-part-one/",
    "https://developer.cyberark.com/blog/retrieving-conjur-secrets-in-a-spring-mvc-kubernetes-application/",
    "https://developer.cyberark.com/blog/using-conjur-rest-openapi-to-simplify-secure-software-development/",
    "https://developer.cyberark.com/blog/setting-up-conjur-on-openshift/",
    "https://developer.cyberark.com/blog/installing-conjur-in-an-eks-kubernetes-cluster-using-rancher/",
    "https://developer.cyberark.com/blog/conjur-secrets-management-in-knative-serverless-functions/",
    "https://developer.cyberark.com/blog/using-cyberark-conjur-with-azure-serverless-functions-and-managed-identities/",
    "https://developer.cyberark.com/blog/tutorial-kubernetes-vulnerability-scanning-testing-with-open-source/",
    "https://developer.cyberark.com/blog/new-red-hat-openshift-secrets-management-operator-for-the-conjur-follower/",
    "https://developer.cyberark.com/blog/low-code-secrets-management-for-beginners/",
    "https://developer.cyberark.com/blog/technical-deep-dive-centralized-secrets-management-for-multi-cloud-with-infrastructure-as-code/",
    "https://developer.cyberark.com/blog/remove-secrets-from-your-codebase/",
    "https://developer.cyberark.com/blog/iot-and-edge-secrets-management-with-conjur-and-k3s/",
    "https://developer.cyberark.com/blog/why-machine-identity-is-as-important-as-user-identity-to-infrastructure-security/",
    "https://developer.cyberark.com/blog/three-steps-to-avoiding-the-secret-zero-trap/",
    "https://developer.cyberark.com/blog/managing-testing-secrets-in-jenkins-pipelines/",
    "https://developer.cyberark.com/blog/adding-conjur-secrets-management-to-your-jenkins-pipeline/",
    "https://developer.cyberark.com/blog/keeping-secrets-secure-on-kubernetes/",
    "https://developer.cyberark.com/blog/why-you-need-secrets-management-in-your-jenkins-pipeline/",
    "https://developer.cyberark.com/blog/kubernetes-secrets-management-build-secure-apps-faster-without-secrets/",
]

#url_list = ['https://docs.cyberark.com/conjur-cloud/latest/en/Content/Resources/_TopNav/cc_Home.htm']

pd = pd.DataFrame(columns=["Url","Text"])
for i in range(len(url_list)):
    read_url = url_list[i]
    req = Request(url=read_url, headers={'User-Agent': 'Mozilla/5.0'})
    mybytes = urlopen(req).read()
    mystr = mybytes.decode("utf8")
    pd.loc[i] = [read_url, remove_tags(mystr)]

pd.to_csv("./ConjurBlogArticles.csv")
