# https://cloud.google.com/natural-language/docs/basics

from google.cloud import language_v1

from .category import transform_category


def _analyze_sentiment(client, text):
    document = {'content': text, 'language': 'en', 'type_': language_v1.Document.Type.PLAIN_TEXT}

    response = client.analyze_sentiment(request={'document': document})

    return {
        'score': response.document_sentiment.score,
        'magnitude': response.document_sentiment.magnitude,
    }

def _classify_text(client, text):
    content_categories_version = language_v1.ClassificationModelOptions.V2Model.ContentCategoriesVersion.V2
    document = {'content': text, 'language': 'en', 'type_': language_v1.Document.Type.PLAIN_TEXT}

    response = client.classify_text(
        request={
            'document': document,
            'classification_model_options': {
                'v2_model': {
                    'content_categories_version': content_categories_version
                }
            }
        }
    )

    result = [{
        'category_original': category.name,  # https://cloud.google.com/natural-language/docs/categories
        'category': transform_category(category.name),
        'confidence': category.confidence,
    } for category in response.categories]

    if not result:
        result = [{'cetegory': 'General', 'confidence': 0.5}]   # broad, wide

    return result

def _analyze_entity_sentiment(client, text):
    document = {'content': text, 'language': 'en', 'type_': language_v1.Document.Type.PLAIN_TEXT}

    response = client.analyze_entity_sentiment(request={'document': document})

    result = []
    for entity in response.entities:
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        entity_type = language_v1.Entity.Type(entity.type_).name
        # Get the salience score associated with the entity in the [0, 1.0] range
        score = entity.salience
        sentiment = entity.sentiment
        data = {
            'type': entity_type,
            'score': score,
            'sentiment_score': sentiment.score,
            'sentiment_magnitude': sentiment.magnitude,
            'mentions': [{
                'type': language_v1.EntityMention.Type(mention.type_).name,
                'text': mention.text.content,
            } for mention in entity.mentions],
        }
        result.append(data)

    return result


def analyze_text(text):
    client = language_v1.LanguageServiceClient.from_service_account_json('service-account.json')

    return {
        'categories': _classify_text(client, text),
        'entities': _analyze_entity_sentiment(client, text),
        'sentiment': _analyze_sentiment(client, text),
    }
