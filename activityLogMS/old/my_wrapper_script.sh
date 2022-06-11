#!/bin/bash

# Start the first process
python ./amqp_setup.py &
  
# Start the second process
python ./activity_log.py &

# Start the thrid process
python ./error.py &

  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?