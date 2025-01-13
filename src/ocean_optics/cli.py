import typer
from rich import print
from rich.table import Table

from ocean_optics.spectroscopy import DeviceNotFoundError, SpectroscopyExperiment

app = typer.Typer()


@app.command()
def check():
    """Check if a compatible device can be found."""
    try:
        SpectroscopyExperiment()
    except DeviceNotFoundError:
        print("[red]No compatible device found.")
    else:
        print("[green]Device is connected and available.")


@app.command()
def spectrum():
    """Show a spectrum."""
    experiment = open_experiment()

    wavelengths, intensities = experiment.get_spectrum()
    table = Table("Wavelength (nm)", "Intensity")
    for wavelength, intensity in zip(wavelengths, intensities):
        table.add_row(f"{wavelength:.1f}", f"{intensity:.1f}")
    print(table)


def open_experiment():
    """Open the spectroscopy experiment.

    Connect to an available spectropy device.

    Raises:
        typer.Abort: An error occured opening the experiment.

    Returns:
        An `ocean_optics.Spectroscopy` instance.
    """
    try:
        experiment = SpectroscopyExperiment()
    except DeviceNotFoundError:
        print("[red]No compatible device found.")
        raise typer.Abort()
    return experiment


if __name__ == "__main__":
    app()
