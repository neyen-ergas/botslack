x=datetime.today()
    y = x.replace(day=x.day, hour=14, minute=28, second=0, microsecond=0) + timedelta(days=0)
    delta_t=y-x

    secs=delta_t.total_seconds()

    def hello_world():
        print ("hello world")
        

    t = Timer(secs, hello_world)
    t.start()
    