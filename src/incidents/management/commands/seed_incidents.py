"""Management command that fills the database with sample incidents."""

import random
from datetime import timedelta
from typing import Any, TypedDict

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.utils import timezone

from incidents.models import Incident


class IncidentFamily(TypedDict):
    """Wording variants of one kind of problem, mixed at random to build incidents."""

    equipment: list[str]
    titles: list[str]
    descriptions: list[str]


# Titles and descriptions are combined freely within a family, so the generated
# data contains near-duplicates that share vocabulary — the kind of incidents a
# similarity model is expected to find.
INCIDENT_FAMILIES: list[IncidentFamily] = [
    {
        "equipment": ["Switch-12", "Switch-07", "Router-Core", "Switch-3F"],
        "titles": [
            "Network outage in building B",
            "No network connectivity on the 3rd floor",
            "Network down in the sales office",
            "Intermittent network drops",
        ],
        "descriptions": [
            "Users in building B report no network connectivity since this morning; the switch link LEDs are off.",
            "Several workstations on the 3rd floor lost network access; cables and patch panel look fine.",
            "The whole sales office is without network; the switch port LEDs are blinking amber.",
            "The network connection drops for a few seconds every couple of minutes across the floor.",
        ],
    },
    {
        "equipment": ["Printer-2F", "Printer-Lobby", "Printer-HR", "Plotter-Design"],
        "titles": [
            "Printer not printing",
            "Printer on 2nd floor shows paper jam",
            "Print jobs stuck in the queue",
            "Printer offline",
        ],
        "descriptions": [
            "The printer accepts print jobs but nothing comes out; the display shows a paper jam error although there is no paper inside.",
            "All print jobs sent to the printer stay stuck in the queue and never print.",
            "The printer appears offline on every workstation even though it is powered on and connected.",
            "Printing produces blank pages; toner level reads 60 percent.",
        ],
    },
    {
        "equipment": ["Laptop-A102", "Laptop-B215", "Laptop-C044", "Laptop-D310"],
        "titles": [
            "Laptop does not boot",
            "Laptop battery drains very fast",
            "Laptop is extremely slow",
            "Laptop screen flickers",
        ],
        "descriptions": [
            "The laptop shows a black screen after the manufacturer logo and never reaches the login screen.",
            "The laptop battery goes from 100 to 10 percent in under an hour even when idle.",
            "The laptop takes more than ten minutes to boot and every application freezes for seconds.",
            "The laptop screen flickers and shows horizontal lines, especially when the lid is moved.",
        ],
    },
    {
        "equipment": ["Server-01", "Server-02", "DB-Server", "Backup-Server"],
        "titles": [
            "Server down",
            "Server unreachable",
            "Server running out of disk space",
            "Server CPU at 100 percent",
        ],
        "descriptions": [
            "The main server is unreachable; ping and SSH time out and the hosted services are down.",
            "The server stopped responding after the nightly backup; the console shows a kernel panic.",
            "The server disk is at 98 percent usage and the database refuses to write new records.",
            "The server CPU has been pinned at 100 percent for hours and every request times out.",
        ],
    },
    {
        "equipment": ["Mail-Server", "Exchange-01", "Outlook", "Webmail"],
        "titles": [
            "Cannot send emails",
            "Emails not being received",
            "Outlook keeps asking for the password",
            "Email delivery delayed",
        ],
        "descriptions": [
            "Outgoing emails stay in the outbox and Outlook reports the SMTP server is not responding.",
            "No emails have been received since yesterday afternoon; senders get no bounce message.",
            "Outlook prompts for the password every few minutes and refuses to connect to the mail server.",
            "Emails arrive several hours late; the mail server queue keeps growing.",
        ],
    },
    {
        "equipment": ["VPN-Gateway", "VPN-Client", "Firewall-01", "VPN-Backup"],
        "titles": [
            "VPN connection fails",
            "Cannot connect to VPN from home",
            "VPN disconnects every few minutes",
            "VPN authentication error",
        ],
        "descriptions": [
            "The VPN client fails to connect with a timeout error when working from home.",
            "The VPN connects but drops every few minutes, forcing remote users to reconnect.",
            "VPN login fails with an authentication error although the credentials are correct.",
            "The VPN gateway rejects new connections; existing sessions still work.",
        ],
    },
    {
        "equipment": [
            "Monitor-Desk-14",
            "Monitor-Room-B",
            "Monitor-Desk-27",
            "Projector-Meeting",
        ],
        "titles": [
            "Monitor shows no signal",
            "Monitor display is flickering",
            "Second monitor not detected",
            "Monitor colors look wrong",
        ],
        "descriptions": [
            "The monitor shows a no signal message even though the HDMI cable is connected on both ends.",
            "The monitor display flickers and goes black for a second every few minutes.",
            "The second monitor is not detected by the laptop after the last driver update.",
            "The monitor shows a strong pink tint; colors look wrong on every input.",
        ],
    },
    {
        "equipment": ["Office-365", "Adobe-Suite", "AutoCAD", "Antivirus"],
        "titles": [
            "Software license expired",
            "Cannot activate the software license",
            "Application shows license error at startup",
            "License server not reachable",
        ],
        "descriptions": [
            "The application refuses to start and shows a license expired message.",
            "License activation fails with an error saying the license server is not reachable.",
            "The software opens in read-only mode because the license could not be validated.",
            "Every user gets a license error at startup since the license server was rebooted.",
        ],
    },
    {
        "equipment": ["WiFi-AP-1F", "WiFi-AP-2F", "WiFi-Guest", "WiFi-Warehouse"],
        "titles": [
            "Wi-Fi not working on the 1st floor",
            "Wi-Fi signal very weak",
            "Cannot connect to the guest Wi-Fi",
            "Wi-Fi keeps disconnecting",
        ],
        "descriptions": [
            "Nobody on the 1st floor can connect to the Wi-Fi; the access point LED is red.",
            "The Wi-Fi signal is very weak in the meeting rooms and video calls keep freezing.",
            "Visitors cannot connect to the guest Wi-Fi; the captive portal never loads.",
            "Laptops keep disconnecting from the Wi-Fi and reconnecting every few minutes.",
        ],
    },
    {
        "equipment": ["NAS-01", "FileServer", "SharePoint", "Shared-Drive-Finance"],
        "titles": [
            "Cannot access the shared drive",
            "Shared folder permission denied",
            "Shared drive very slow",
            "Files missing from the shared drive",
        ],
        "descriptions": [
            "The shared drive does not mount at login and the path shows a network path not found error.",
            "Users get permission denied when opening files on the shared finance folder.",
            "Opening or saving files on the shared drive takes minutes; local files are fine.",
            "Several files disappeared from the shared drive overnight; the backup may need restoring.",
        ],
    },
]

PRIORITY_WEIGHTS = {
    Incident.Priority.LOW: 30,
    Incident.Priority.MEDIUM: 45,
    Incident.Priority.HIGH: 25,
}
STATUS_WEIGHTS = {
    Incident.Status.OPEN: 45,
    Incident.Status.IN_PROGRESS: 25,
    Incident.Status.CLOSED: 30,
}
ARCHIVED_RATIO = 0.1


class Command(BaseCommand):
    """Create sample incidents so the dashboards and the ML notebook have data to work with.

    Incidents are built from :data:`INCIDENT_FAMILIES`, assigned at random to the
    existing users and spread over the last ``--days`` days. The command is not
    idempotent: every run adds ``--count`` new incidents.
    """

    help = "Fill the database with randomly generated sample incidents."

    def add_arguments(self, parser: CommandParser) -> None:
        """Register the ``--count``, ``--seed`` and ``--days`` options.

        :param parser: The argument parser for this command.
        """
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of incidents to create (default: 100).",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Random seed, for reproducible output.",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Spread registration dates over the last N days (default: 90).",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Generate and save the requested number of incidents.

        :param args: Unused positional arguments.
        :param options: Parsed command options (``count``, ``seed``, ``days``).
        :raises CommandError: If there are no users to own the incidents.
        """
        users = list(get_user_model().objects.order_by("pk"))
        if not users:
            raise CommandError("Create at least one user before seeding incidents.")

        rng = random.Random(options["seed"])
        count: int = options["count"]
        days: int = options["days"]
        now = timezone.now()

        incidents = [self.build_incident(rng, users) for _ in range(count)]
        Incident.objects.bulk_create(incidents)

        # ``date`` is auto_now_add, so it can only be backdated after the insert.
        for incident in incidents:
            incident.date = now - timedelta(seconds=rng.uniform(0, days * 86400))
        Incident.objects.bulk_update(incidents, ["date"])

        self.stdout.write(self.style.SUCCESS(f"Created {count} sample incidents."))

    def build_incident(self, rng: random.Random, users: list[Any]) -> Incident:
        """Build one unsaved incident from a random family and wording variants.

        :param rng: The random generator, so results are reproducible with ``--seed``.
        :param users: Existing users; one is picked at random as the reporter.
        :return: An unsaved :class:`Incident` instance.
        """
        family = rng.choice(INCIDENT_FAMILIES)
        return Incident(
            title=rng.choice(family["titles"]),
            description=rng.choice(family["descriptions"]),
            equipment=rng.choice(family["equipment"]),
            priority=rng.choices(
                list(PRIORITY_WEIGHTS), weights=list(PRIORITY_WEIGHTS.values())
            )[0],
            status=rng.choices(
                list(STATUS_WEIGHTS), weights=list(STATUS_WEIGHTS.values())
            )[0],
            is_archived=rng.random() < ARCHIVED_RATIO,
            user=rng.choice(users),
        )
