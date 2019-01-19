(python create_docs.py) & \
(export FLASK_APP=run.py && \
export FLASK_DEBUG=1 && \
flask run)

wait
echo "Kiling the flask server"
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

