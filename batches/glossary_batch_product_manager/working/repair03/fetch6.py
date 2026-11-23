exec(open('batches/glossary_batch_product_manager/working/repair03/fetch.py').read().split('urls=')[0])
urls={
'flagmonitor':'https://www.atlassian.com/agile/software-development/software-deployment',
'flagmonitor2':'https://www.atlassian.com/software-development/practices/feature-flagging',
'flagmonitor3':'https://www.atlassian.com/blog/development/tips-for-feature-flagging',
'position5':'https://www.productplan.com/glossary/product-positioning',
'dependency':'https://www.atlassian.com/agile/project-management/project-management-dependencies',
'capacity':'https://www.atlassian.com/agile/product-management/product-planning'
}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:list(e.map(fetch,urls.items()))
