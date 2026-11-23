exec(open('batches/glossary_batch_product_manager/working/repair03/fetch.py').read().split('urls=')[0])
urls={
'values4':'https://www.atlassian.com/blog/innovation/company-culture-company-values',
'job5':'https://www.nngroup.com/articles/jobs-to-be-done',
'job6':'https://www.nngroup.com/articles/personas-jobs-be-done/',
'job7':'https://www.atlassian.com/agile/product-management/jobs-to-be-done-framework',
'pmf6':'https://amplitude.com/blog/analytics-product-market-fit',
'pmf7':'https://amplitude.com/books/mastering-retention/why-you-need-to-care-about-user-retention',
'pmf8':'https://www.productplan.com/learn/how-to-measure-product-market-fit',
'release6':'https://www.productplan.com/learn/product-roadmap-vs-release-plan',
'release7':'https://www.productplan.com/learn/how-to-quarterly-release-plan',
'market6':'https://www.atlassian.com/agile/product-management/tam-sam-som',
'position4':'https://www.atlassian.com/work-management/project-management/positioning-statement',
'flagoverview':'https://amplitude.com/docs/feature-experiment/overview'
}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:list(e.map(fetch,urls.items()))
