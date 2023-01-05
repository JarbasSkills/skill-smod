#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-smod.jarbasai=skill_smod:SMODSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-smod',
    version='0.0.1',
    description='ovos black metal skill plugin',
    url='https://github.com/JarbasSkills/skill-smod',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_smod": ""},
    package_data={'skill_smod': ['locale/*', 'ui/*', 'res/*']},
    packages=['skill_smod'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
