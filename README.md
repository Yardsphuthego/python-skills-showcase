# Python & Networking Skills Showcase

**Mmoloki Phuthego · Network Computing Student · Full Stack Python Developer**

Gaborone, Botswana · [GitHub profile](https://github.com/Yardsphuthego) · [Email](mailto:ns24-035@thuto.bac.ac.bw)

**Available for industrial attachment: 11 January – 30 June 2027**

I'm a third-year BSc (Hons) Network Computing student at Botswana Accountancy College. Networking is my primary specialisation, alongside Python backend development, network automation, and cloud deployment. I'm seeking attachment in a software or fintech team where I can contribute across development and infrastructure.

This portfolio brings together runnable Python examples, selected project summaries, and my networking background. The Python examples are simplified adaptations of patterns from my private backend work.

## Start Here

- **Review my Python:** [wallet logic](src/showcase/wallet.py), [payment workflows](src/showcase/payments.py), [reporting](src/showcase/reporting.py), and [message encryption](src/showcase/message_crypto.py).
- **Explore my projects:** [selected project portfolio](docs/projects.md), covering commerce, healthcare workflows, civic services, developer tools, USSD, voting, and water infrastructure.
- **Review my networking background:** [networking, automation, and Cisco training](docs/networking.md).
- **Try the examples:** use the setup instructions below and run the [tests](tests/).

## Python Examples

| Example | What you can review | Tests |
| --- | --- | --- |
| [Wallet](src/showcase/wallet.py) | Dataclasses, Decimal balances, PIN checks, transfer validation, spending limits, transaction snapshots | [Wallet tests](tests/test_wallet.py) |
| [Payments](src/showcase/payments.py) | Provider availability, fee calculation, Botswana phone formatting, withdrawal limits, connector interfaces | [Payment tests](tests/test_payments.py) |
| [Reporting](src/showcase/reporting.py) | Monthly order aggregation, sales summaries, refunds, product and inventory metrics | [Reporting tests](tests/test_reporting.py) |
| [Messaging](src/showcase/message_crypto.py) | Fernet encryption/decryption and configurable keys | [Encryption test](tests/test_message_crypto.py) |

[Read the walkthroughs and original project context](docs/python-examples.md).

These are educational, in-memory examples. They do not process live payments or provide production wallet storage. The messaging helper includes plaintext fallback behaviour; see the [demo boundaries](docs/python-examples.md#demo-boundaries).

## Networking & Infrastructure

- **Networking:** VLANs, OSPF, IPv4/IPv6 addressing, ACLs, NAT, and network security fundamentals.
- **Automation:** Python, Netmiko, Cisco pyATS, and Genie.
- **Cloud & systems:** application deployment and live environment management on AWS and Microsoft Azure; Linux, domain configuration, and DNS.
- **Hands-on practice:** a personal local server, Nmap, and website security testing.

### Cisco Networking Academy — Course Completions

| Course | Completion |
| --- | --- |
| CCNA 1: Introduction to Networks | Completed |
| CCNA 3: Enterprise Networking, Security, and Automation | 7 September 2026 |

These are Cisco Networking Academy course completions, not a claim of the full CCNA certification. Networking skills are described in the [networking overview](docs/networking.md); this repository currently contains Python backend examples rather than device configurations or automation lab submissions.

## Selected Projects

| Project | Focus | Review |
| --- | --- | --- |
| | Django commerce, wallets, payments, and reporting | [Summary and Python examples](docs/projects.md#commerce-and-payment-platform) |
| MedLocate | Medicine inventory, validated Excel imports, and prescription workflows | [Project summary](docs/projects.md#medlocate) |
| TEBELO | Geospatial incident reporting and public-service delivery workflows | [Project summary](docs/projects.md#tebelo) |
| BOPA | Visual IDE with Django/React code generation and learning tools | [Project summary](docs/projects.md#bopa) |
| CAR_PARTS search | FastAPI car-parts platform with USSD search and Redis session handling | [Project summary](docs/projects.md#carmavunaparts) |
| THUTO student voting | FastAPI election APIs and React interfaces | [Summary and public code](docs/projects.md#student-voting-system) |
| TAIMS Platform | Water-storage assets, inspections, work orders, and reporting | [Public repository](https://github.com/Yardsphuthego/taims-platform) |
| Food inflation forecasting | AI forecasting project described in my CV | [Project summary](docs/projects.md#food-inflation-forecasting) |

Demonstrations and selected code walkthroughs for private projects are available on request.

## Run Locally

Requires **Python 3.11 or newer**.

```bash
git clone https://github.com/Yardsphuthego/python-skills-showcase.git
cd python-skills-showcase
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
```

On Windows, create the environment with `py -m venv .venv` and activate it in PowerShell with `.venv\Scripts\Activate.ps1`, then run the same install and test commands.

## Education & Skills

**Botswana Accountancy College, Gaborone**

BSc (Hons) Network Computing · Year 3 · Full-time

Expected completion: **July 2028**

Current modules: Computer Systems Administration, Enterprise Networking, and Network Security.

| Area | Technologies |
| --- | --- |
| Backend & data | Python, Django, Django REST Framework, FastAPI, SQLAlchemy, PostgreSQL, Redis |
| Application development | Flutter, React, TypeScript, Next.js, Tauri |
| Machine learning | PyTorch |
| Containers & infrastructure | Docker, Kubernetes, AWS, Microsoft Azure, Linux |
| Technical documentation | LaTeX |

## Achievement

**Top 10 finalist — 2025/26 BAC Student Investment Battlefield**, with **Small Yachts**. Selected from 59 entries to progress to the incubation stage.

## Attachment & Contact

Available **11 January – 30 June 2027** for industrial attachment.

For opportunities, project demonstrations, or selected code walkthroughs, contact **[ns24-035@thuto.bac.ac.bw](mailto:ns24-035@thuto.bac.ac.bw)**.
