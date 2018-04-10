def parse_list_message(message):
    response, *content = message.split('\n')
    response = ' '.join(response.split(' ')[1:])

    result_content = [line.split(' ') for line in content]

    return response, result_content
