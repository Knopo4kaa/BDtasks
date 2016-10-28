from amazonproduct import API
config = {
    'access_key': 'AKIAJEO5KDIOOA3WQEDA',
    'secret_key': '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',
    'associate_tag': 'redtoad-10',
    'locale': 'us'
}
api = API(cfg=config)

for book in api.item_search('Books', Publisher='Galileo Press'):
    print ('{}: "{}"'.format(book.ItemAttributes.Author, book.ItemAttributes.Title))