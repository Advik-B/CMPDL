

@click.command()
@click.option(
    '-o',
    '--output',
    default=os.path.join(
        os.path.expanduser(
            '~'
            ),
        'mods'
        ),
    help='Output file'
    )
@click.option(
    '-f',
    '--file',
    help='Input file (REQUIRED)',
    required=True,
    )
@click.option(
    '-d',
    '--download-optional',
    is_flag=True,
    help='Download optional mods'
    )
@click.option(
    '-k',
    '--keep-config',
    is_flag=True,
    help='Keep config file(s) in output folder (If any)'
    )
def main(output, file, download_optional, keep_config):
    global logger
    logger_ = logger.Logger()
    # Prep the kwargs
    kwargs = {
        'log_func': logger_.log,
        'secondry_log': logger_.log,
        'output_dir': output,
        'download_optional': download_optional,
        'keep_config': keep_config
    }
    # Create the ModPack object
    try:
        m = ModPack(file, **kwargs)
        m.init()
        m.install()
    except Exception as e:
        print(e)
        print("Something went wrong, check the log for more info")
        print("If you think this is a bug, please report it on the GitHub page")
        print("https://github.com/Advik-B/CMPDL/issues/new")
        raise e from e
    finally:
        logger_.quit()

if __name__ == '__main__':
    main()
