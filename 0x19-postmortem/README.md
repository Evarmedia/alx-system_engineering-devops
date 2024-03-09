# Postmortem

At around 06:00AM West African Time (WAT) in Nigeria, an outage was detected on an isolated Ubuntu 14.04 - 293 sandbox container hosting an Apache web server following the release of ALX's System Engineering & DevOps project 0x19. Instead of the anticipated response, which was supposed to be an HTML file defining a basic Holberton WordPress site, GET requests on the server were resulting in 500 Internal Server Errors.

## Debugging Process

I, Mishak Mosimabale encountered the issue upon opening the project and being, well, instructed to address it, roughly 9:43AM WAT. He promptly proceeded to undergo solving the problem.

1. Initial Freak-Out Moment: When I stumble upon a bug, my heart skips a beat, but then I remind myself that bugs fear my debugging prowess. I quickly brew a strong cup of coffee (extra shots, please) to prepare for the impending battle.

2. Sherlock Holmes Mode: I become the Sherlock of my codebase, scouring logs, revisiting recent changes, and interrogating my code like a seasoned detective. Bugs may be elusive, but they can't hide from my keen eye!

3. Java Jive Break: Midway through the investigation, I take a Java jive break (yes, I'm a coffee aficionado) to let my brain simmer and stew over the problem. Sometimes, the best solutions come when you're least expecting them—usually between sips of caffeine.

4. And thus began the actual process of debugging, I Checked running processes using `ps aux`. Two `apache2` processes - `root` and `www-data` -
were running properly.

5. Looked in the `sites-available` folder of the `/etc/apache2/` directory. Determined that
the web server was serving content located in `/var/www/html/`.

6. I launched strace in one terminal to trace the activities of the root Apache process using its PID. Simultaneously, in another terminal, I sent a curl request to the server, hoping for enlightening results. Alas, my expectations were dashed as strace yielded no helpful insights.

4. Repeated step 4, except on the PID of the `www-data` process. Kept expectations lower this
time... but was rewarded! `strace` revelead an `-1 ENOENT (No such file or directory)` error
occurring upon an attempt to access the file `/var/www/html/wp-includes/class-wp-locale.phpp`.

5. Looked through files in the `/var/www/html/` directory one-by-one, using Vim pattern
matching to try and locate the erroneous `.phpp` file extension. Located it in the `wp-settings.php` file. (Line 137, `require_once( ABSPATH . WPINC . '/class-wp-locale.php' );`).

6. I used "grep -ro "phpp" /var/www/html" and "grep -n "phpp" /var/www/html/wp-settings.php" to check the lines 

7. I then fixed the typo error `p` from the line.

8. Tested another `curl` on the server. And it was OK.

9. Finally Wrote a Puppet manifest to automate fixing of the error.

## Summation

In short, it was a classic case of a typo wreaking havoc. The WordPress app hit a critical snag in wp-settings.php while attempting to access class-wp-locale.phpp instead of the correct file, class-wp-locale.php, nestled snugly in the wp-content directory.

The fix was straightforward—just snip the extra 'p' from the file name.

## Prevention
This hiccup wasn't a server mishap but an app blunder. To dodge similar mishaps in the future, here are some pointers:

Testing, testing, 1-2-3. Run rigorous tests pre-deployment. Catching this typo earlier would have nipped the issue in the bud.
Stay vigilant. Employ uptime monitoring tools like UptimeRobot to pounce on website outages pronto.

