exec(open('batches/glossary_batch_product_manager/working/repair03/fetch.py').read().split('urls=')[0])
urls={
'market5':'https://www.productplan.com/glossary/total-addressable-market',
'release4':'https://www.productplan.com/glossary/release-plan',
'releasemgmt3':'https://www.productplan.com/glossary/release-management',
'flags4':'https://amplitude.com/docs/feature-experiment/workflow/feature-flag-rollouts',
'pmf5':'https://www.romanpichler.com/blog/achieving-product-market-fit/',
'release5':'https://www.romanpichler.com/blog/agile-release-planning/',
'jtbd4':'https://www.atlassian.com/blog/productivity/job-stories',
'values3':'https://www.atlassian.com/work-management/strategic-planning/mission-and-vision',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:list(e.map(fetch,urls.items()))
