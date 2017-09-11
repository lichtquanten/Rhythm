# Rhythm

## Inspiration.
As technology becomes more and more relevant in todays society, a recent rise in popularity has been in the financial technology sector, more specifically Algorithmic trading. However Algorithmic Trading is very complicated for most people, it requires years of knowledge of stocks, investing and programming skills. We wanted to remove these barriers and make Algorithm trading available for everyone and make it as simple as possible.

## So what did we do?
We built a direct English sentence to algorithm generator. We used Natural Language processing to analyze a regular sentence and then gave that to a compiler we built, which would generate an investment algorithm. We then leverage Quantopian, and Zipline to leverage historical stock data and run the generated algorithm against it. We then use various python data visualization libraries to display this data in an intuitive and informational way. This allows user to get a preview of how their algorithm would perform in the real world. Thus allowing the average person, high schooler and even middle schooler participate in algorithmic trading.

## Challenges we ran into:
Along the way we ran into many challenges, some more frustrating than others. One of the biggest challenges we ran into was a github issue. For some reason, one of our teammate's invitation had bugged, and caused for our entire version history to experience bugs. For example, we rolled back one commit, however, we would end up rolling back 3 commits. This was reproduced many times and we never found a clear solution to fix issues with our GitHub. Another issue we had was having our home built compiler be able to handle as many possible forms of trading. This was an iterative process, in which we ended up finding many different cases that our compiler wouldn’t properly build the right algorithm for. However, by the end, we managed to build a generalized solution, which works for almost every scenario.

## Accomplishments that we’re proud of:
Our entire project was very involved, we had a web app, a natural language processing section and data visualization. These parts had to work together flawlessly to accomplish what wanted, and though we ran close on time, we were able to get everything interacting how we wanted, and we are really proud of that. Also pulling off our own compiler and natural language processing is something we are really happy to have been able to do.

## What we learned:
We learned a lot over the weekend, everything from how to properly analyze text using natural language processing, to how to build our own compiler and having two very different web technologies work together.

## What’s next for Rhythm:
Though we were able to add a lot of cool features, there is a lot more to investing and from here we want to make our natural language processing more sophisticated so that it can handle more complex investment techniques and properly generate the algorithm. Another goal within our sites, is to build an added layer, so that our investment algorithm can interact with stocks in real-time and we can monitor that data, without spending real money. This would be very huge, as then you would have 2 data points, one being historical data and another being the live stock prices.

