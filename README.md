# IXP Valuator

## Use cases

1. Local eye-balls to local content in a country
2. From members/non-members of an IXP to content in a country
3. To show value of the creation of an IXP (perhaps time-based)
4. From Local probes to country's content (to detect if reaching that content stays in the country)

## Methodology

1. Carefully select sources and destinations
2. Run traceroutes from sources to destinations
3. Analyze traceroutes by tagger
4. Extract meaningful metric from traceroutes
5. Visualize aggregate results in some way

## Examples

Fire up a local HTTP server (you can use Python) and load the
visualization code:

```
python2 -m SimpleHTTPServer 3333
```

The following cases are included

1. [http://localhost:3333/visualize.html?namex-aggregated.json](Namex IXP Customer Analysis)
2. Argentina's Local Content
3. Italy's Local Content
4. Cabase IXP Customer Analysis
5. Senegal's In/Out Country Analysis
6. Sweden's Local Content
7. Kenya's Local Content

