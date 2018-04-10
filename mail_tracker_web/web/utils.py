def parse_list_message(message):
    response, *content = message.split('\n')
    response = ' '.join(response.split(' ')[1:])

    result_content = []

    for item in content:
        if not len(item) > 0:
            continue

        subject, item_id = item.split(' ')

        result_content.append({
            'subject': subject,
            'id': item_id
        })

    print(result_content)

    return response, result_content
