exec(open('batches/glossary_batch_product_manager/working/repair03/fetch.py').read().split('urls=')[0])
urls={
'retention1':'https://amplitude.com/blog/measure-user-retention',
'retention2':'https://amplitude.com/blog/understanding-user-retention',
'retention3':'https://amplitude.com/explore/analytics/retention-curve',
'retention4':'https://amplitude.com/blog/retention-product-strategy',
'flagstages':'https://www.productplan.com/blog/structuring-feature-rollouts-to-maximize-product-adoption',
'atsother':'https://www.atlassian.com/sitemaps/other.xml',
'atsresources':'https://www.atlassian.com/sitemaps/resources.xml',
'joblearn':'https://www.productplan.com/learn/jobs-to-be-done-framework'
}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:list(e.map(fetch,urls.items()))
