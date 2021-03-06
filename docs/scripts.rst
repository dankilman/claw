=======
Scripts
=======
The script mechanism allows you to execute python scripts through ``claw``
and import a context object named ``cosmo``.

Executing Scripts
-----------------
There are several ways to execute scripts:

#.
    Explicit path to the script:

    .. code-block:: sh

        $ claw script {CONFIGURATION_NAME} {PATH_TO_SCRIPT}

    The above will execute the script located at ``{PATH_TO_SCRIPT}`` with the
    configuration ``CONFIGURATION_NAME`` as its ``cosmo`` (context).

#.
    If a script is located under ``$CLAW_HOME/scripts`` (or any other scripts
    dir that is explicitly added to the ``~/.claw``, ``scripts`` setting), it can be
    executed less verbosely by specifying the filename only without the full path,
    for example if there is a
    script named ``my_script.py`` under ``$CLAW_HOME/scripts``, it can be executed by
    running:

    .. code-block:: sh

        $ claw script {CONFIGURATION_NAME} my_script.py

    If the script name ends with ``.py`` you can omit the ``.py`` extension:

    .. code-block:: sh

        $ claw script {CONFIGURATION_NAME} my_script

    If the script name ends with ``.py`` you can also run it as if it were a
    built-in ``claw`` command (underscores ``_`` are replaced with dashes ``-``):

    .. code-block:: sh

        $ claw my-script {CONFIGURATION_NAME}


#.
    To enable running scripts directly, ``claw`` will execute a script if it's
    path is supplied as the first argument, e.g.:

    .. code-block:: sh

        $ claw {PATH_TO_SCRIPT}

    If called like this, the active configuration represented by
    the ``cosmo`` context, will be of the configuration that was ``claw generate``-ed or
    ``claw bootstrap``-ed most recently.

    .. tip::
        By adding ``#! /usr/bin/env claw`` as the first line of an executable script,
        a script can be executed by calling it directly.

        .. code-block:: sh

            $ {PATH_TO_SCRIPT}

Script Functions
----------------
When a script is executed, if no function name is supplied as an additional
argument, a function named ``script`` is searched for, and executed if found.

If a function name is supplied, e.g.

.. code-block:: sh

    $ claw script {CONFIGURATION_NAME} {SCRIPT_PATH} my_function

it will be executed instead (``my_function`` in the example above).

Script Function Arguments
-------------------------
Functions are executed by leveraging the ``argh`` library. This library makes it
easy to pass additional configuration to the function with very little effort
in terms of argument parsing.

For example, consider the following script

.. code-block:: python

    #! /usr/bin/env claw

    def script(first_name, last_name, age=35):
        pass

Running the script with no arguments:

.. code-block:: sh

    $ {PATH_TO_SCRIPT}

    usage: claw [-h] [-a AGE] first-name last-name
    claw: error: too few arguments

You can also run help:

.. code-block:: sh

    $ {PATH_TO_SCRIPT} --help

    usage: claw [-h] [-a AGE] first-name last-name

    positional arguments:
      first-name         -
      last-name          -

    optional arguments:
      -h, --help         show this help message and exit
      -a AGE, --age AGE  35

As can be seen in the previous snippets, the ``argh`` library will analyze the
function signature and determine that it expects two positional arguments and
one optional argument named ``age``.

If we wanted, we could add help descriptions to all the arguments

.. code-block:: python

    #! /usr/bin/env claw

    import argh

    @argh.arg('first-name', help='The first name')
    @argh.arg('last-name', help='The last name')
    @argh.arg('-a', '--age', help='The age')
    def script(first_name, last_name, age=35):
        pass

Which will then produce

.. code-block:: sh

    $ {PATH_TO_SCRIPT} --help

    usage: claw [-h] [-a AGE] first-name last-name

    positional arguments:
      first-name         The first name
      last-name          The last name

    optional arguments:
      -h, --help         show this help message and exit
      -a AGE, --age AGE  The age (default: 35)


Finally, to run this function:

.. code-block:: sh

    $ {PATH_TO_SCRIPT} John Doe 72


All of the features presented above are exposed by the ``argh`` library, but
it was worth mentioning them here because they could be quite useful.
You can read more about ``argh`` in http://argh.readthedocs.org.

Cosmo
-----
Until now, all we showed, was how to run scripts through ``claw``.
This ability on its own, is not very useful, as one could always run scripts
directly through the ``python`` interpreter.

This is where the ``cosmo`` object comes in. The ``cosmo`` object,
serves as your entry point to... well, the cosmo. It encapulates different
aspects and utils of a Cloudify manager environment, specified by
``CONFIGURATION_NAME``.

To use the ``cosmo`` object, add the following to the script imports:

    .. code-block:: python

        from claw import cosmo

Some useful things that the ``cosmo`` holds:

* ``cosmo.client`` will return a configured Cloudify REST client.

* ``cosmo.ssh`` will configure a fabric env to connect to the Cloudify manager.

    usage example:

    .. code-block:: python

        with cosmo.ssh() as ssh:
            ssh.run('echo $HOME')

* ``cosmo.inputs`` will return the inputs used for bootstrapping.

* ``cosmo.handler_configuration`` is the generated handler_configuration used
  when running system tests locally.

* To see other things exposed by ``cosmo`` take a look at the
  ``claw.configuration:Configuration`` class code.

Script Generation
-----------------
To generate a stub script suitable for execution by ``claw``, run the following:

.. code-block:: sh

    $ claw generate-script {PATH_TO_GENERATED_SCRIPT}

The above will create a template script with a ``script`` function and a
``cosmo`` import already in place.

.. note::
    ``claw init`` generates a script named ``example-script.py`` under
    ``$CLAW_HOME/scripts``.

Contributed Scripts
-------------------

The github repo https://github.com/dankilman/claw-scripts contains additional
scripts that can simplify certain day to day Cloudify development related
tasks.

To use these scripts, clone this repository somewhere and add a
``PATH_TO_CLAW_SCRIPTS_REPO_DIR/scripts`` entry to the ``scripts`` list in
``~/.claw``:

.. code-block:: yaml

    claw_home: ...
    main_suites_yaml: ...
    scripts:
      - ...
      - /path/to/claw-scripts/scripts

You are encouraged to open pull requests with your scripts if you find them
useful enough for a wider audience.
