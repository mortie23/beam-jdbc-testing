# Run a custom Dataflow flex template

## Options

### Using the Run script

```sh
./dataflow-run.sh --env dev --name hellofruit
```

### Dataflow UI

Using the Dataflow user interface you can use the _Create a job from template_ and browse to Custom template JSON that was created in the build step.

Given that our `metadata.json` configuration contained a parameter of `output_table` the first optional parameter is Output table.
