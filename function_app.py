import azure.functions as func
import logging

# .venv는 python의 가상 환경 디렉토리
# .vscode는 visual studio code 설정 파일들이 위치함.
# .functionignore는 Azure Function App을 배포할 때 업로드 하지 않을 파일이나 폴더를 지정함.
# .gitignore는 github에 업로드 하지 않을 파일이나 폴더를 지정함.
# function_app.py Azure Funtion App의 진입점 역할을 함. 여기서 트리거와 바인딩을 설정하거나 비즈니스 로직을 구현.
# host.json은 Function App의 설정을 담당함
# local.settings.json은 로컬 개발 환경에서 사용되는 환경 변수를 설정함.
# requirements.txt는 Function App에서 사용할 라이브러리(패키지)를 지정함. (pip install -r requirements.txt로 설치)

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="test-hub",
                               connection="d2t011eventhub_RootManageSharedAccessKey_EVENTHUB") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))

# 이벤트 허브에서 보낸 이벤트를 eventhub_trigger 함수가 받는 것 관련.
# Azure Portal에서 실습한 것 : Event Hub에 데이터가 수신될 때마다 함수가 호출되는 방식
# VS Code에서 함수를 실행하는 것 : 수동으로 함수만 실행하는 것임. 이거는 이벤트 허브에 메시지가 보내지지는 않는다.
# vs code에서 이미 f5 키를 눌러서 함수를 실행하고 있으면, 다시 vs code에서 excute function을 누르면 이벤트 허브에서 이미 수신기가 점유중이라서 data explorer에서 확인하려고 할 때 에러가 나는 것이다.


# output 바인딩 만들기
@app.function_name(name="eventhub_output")
@app.route(route="eventhub_output", methods=["POST"])
@app.event_hub_output(arg_name="event", event_hub_name="test-hub", 
                      connection="d2t011eventhub_RootManageSharedAccessKey_EVENTHUB")
def eventhub_output(req: func.HttpRequest, event: func.Out[str]) -> func.HttpResponse:
    req_body = req.get_body().decode('utf-8')
    logging.info('HTTP trigger function received a request: %s', req_body)

    event.set(req_body)

    return func.HttpResponse("Event Hub output function executed succesfully.", status_code=200)




# This example uses SDK types to directly access the underlying EventData object provided by the Event Hubs trigger.
# To use, uncomment the section below and add azurefunctions-extensions-bindings-eventhub to your requirements.txt file
# Ref: aka.ms/functions-sdk-eventhub-python
#
# import azurefunctions.extensions.bindings.eventhub as eh
# @app.event_hub_message_trigger(
#     arg_name="event", event_hub_name="test-hub", connection="d2t011eventhub_RootManageSharedAccessKey_EVENTHUB"
# )
# def eventhub_trigger(event: eh.EventData):
#     logging.info(
#         "Python EventHub trigger processed an event %s",
#         event.body_as_str()
#     )
