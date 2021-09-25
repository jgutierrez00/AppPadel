from website import create_app
import threading
from datetime import date
import time
from website.views import reset

app = create_app()


def condition_check_thread():
    while True:
        d2 = date.today()
        if (
            d2.weekday() == "Sabado"
            and d2.hour == 0
            and d2.minute == 0
            and d2.second == 0
        ):
            reset()
        time.sleep(5)


if __name__ == "__main__":
    th = threading.Thread(name="checker", target=condition_check_thread)
    th.setDaemon(True)
    th.start()
    app.run("localhost", debug=True)
