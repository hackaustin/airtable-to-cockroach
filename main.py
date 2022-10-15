import asyncio
from prisma import Prisma
from pyairtable import Table
from os import getenv
from dotenv import load_dotenv
from prisma.enums import *
import prisma.errors
import arrow

load_dotenv()

reg_table = Table(getenv("AIRTABLE_KEY"), "app57E6nIn23rmMHe", "Registrations")
records = reg_table.all()

skills = {
    "beginner": technicalSkill.BEGINNER,
    "intermediate": technicalSkill.INTERMEDIATE,
    "advanced": technicalSkill.ADVANCED
}

sizes = {
    "axs": tShirtSize.AXS,
    "as": tShirtSize.AS,
    "am": tShirtSize.AM,
    "al": tShirtSize.AL,
    "axl": tShirtSize.AXL
}


async def main() -> None:
    db = Prisma()
    await db.connect()
    for rec in records:
        data: Dict = rec['fields']
        bday = arrow.get(data["Birthday"], "YYYY-MM-DD").datetime
        try:
            await db.participant.create(
                data={
                    "email": data['Contact Email'],
                    "name": data['Name'],
                    "dob": bday,
                    "technicalSkill": skills[data['Technical Skill']],
                    "tShirtSize": sizes[data['T-shirt size']],
                    "workshop": data.get("Hosting a Workshop", False),
                    "vaccineStatus": data.get("Vaccination Status", False),
                    "pronouns": data.get("Your pronouns", None),
                    "dietaryRestrictions": data.get("Dietary Restrictions", None)
                },
            )
            print(f"created record for {data['Name']}!")
        except prisma.errors.UniqueViolationError:
            print(f"didnt add {data['Name']} due to duplicate")



if __name__ == "__main__":
    asyncio.run(main())
