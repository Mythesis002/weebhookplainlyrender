from flask import Flask, request, Response
app = Flask(_name_)
@app.route('/my_webhook', methods=['POST'])
def return_response():
    print(request.json);
    ## Do something with the request.json data.
    return Response(status=200)
if _name_ == "_main_": app.run()
