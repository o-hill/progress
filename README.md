# progress
Progress is a simple web server using D3.js to present machine learning training progress in real time. 
Basically tensorboard but it works better for us.

## Set up
1. Clone the repository somewhere.
2. Figure out somewhere to put your progress files:
   * Create a directory (mine is `~/.network_progress`).
   * Edit the appropriate lines in both `training_progress.py` and `schema.py` to reference the correct location.
3. Put `training_progress.py` somewhere you can import it from (`~/local-python/` etc.).
4. Go to `progress/progress` and run `npm install`.
5. The servers should both be ready at this point, so start them:
   * `python server.py` from `progress/server/`.
   * `npm run serve` from `progress/progress/`.
6. Put some CSV files in your progress files directory.
7. Head to `localhost:8080` and watch the training progress!


## Progress Writer
`training_progress.py` implements a `Writer` class that follows your ML model and writes data to a CSV file 
in a separate thread while the model is training. A `Writer` object is instantiated with a
name (`Example_Network`), and a list of column names that it should expect (`MSE`, `Wasserstein Loss`, `Sorenson-Dice`, etc.):

```python
from training_progress import Writer
...
# Add as many losses to the list as you want.
writer = Writer('Example_Network', cols=['Mean Squared Error', 'Wasserstein Loss', 'Sorenson-Dice'])
```

In your training loop, extract the loss at each iteration, and write the array to a csv file like so:

```python
losses = network.train(X, y)
writer.write(losses) # losses should be a numpy array here.
```

The `losses` array needs to be the same size as the `cols` list provided above - that is, you need to provide
a measure for each loss at each iteration of training.

You can also query the writer for the average loss over the last ten iterations:

```python
recent_loss_average = writer.loss()
```

When `writer.write()` is called, the `Writer` object adds the array to the `pandas` dataframe that it uses internally,
and then spins off another thread to write the dataframe to the disk. Threading here makes sense since the operation
is purely I/O.
