import logging
import azure.functions as func
from app.main import main

app = func.FunctionApp()
#UTC 22 is AEST 8am 
@app.schedule(schedule="0 0 22 * * *", arg_name="myTimer",
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    main()