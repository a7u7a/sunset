from async_finance import Finance

print("Starting finance data service")
finance = Finance()
finance.thread.join()  # Th