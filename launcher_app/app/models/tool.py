import json
from pathlib import Path

# TOOL_PATH = Path("launcher_app/app/tools.json")

json_string = """
{
  "powder-diffraction": {
    "name": "Powder Diffraction",
    "description": "NOMAD, POWDER, POWGEN",
    "icon": "mdi-filter-outline",
    "theme": "NeutronsTheme",
    "tools": []
  },
  "single-crystal-diffraction": {
    "name": "Single Crystal Diffraction",
    "description": "CORELLI, DEMAND, IMAGINE, MANDI, TOPAZ, WAND²",
    "icon": "mdi-diamond-outline",
    "theme": "NeutronsTheme",
    "tools": [
      {
        "id": "neutrons_trame_garnet",
        "name": "Garnet",
        "description": "Single Crystal Grapical Advanced Reduction Neutron Event Toolkit",
        "max_instances": 1
      },
      {
        "id": "neutrons_trame_topaz",
        "name": "TOPAZ Data Reduction",
        "description": "TOPAZ Data Reduction Application",
        "max_instances": 1
      }
    ]
  },
  "engineering-diffraction": {
    "name": "Engineering Diffraction",
    "description": "HIDRA, SNAP, VULCAN",
    "icon": "mdi-wrench",
    "theme": "NeutronsTheme",
    "tools": []
  },
  "reflectometry": {
    "name": "Reflectometry",
    "description": "LIQREF, MAGREF",
    "icon": "mdi-angle-obtuse",
    "theme": "NeutronsTheme",
    "tools": [
      {
        "id": "neutrons_reflectometry_refl1d",
        "name": "Refl1D",
        "description": "1-D Reflectometry Modeling Program",
        "max_instances": 1
      }
    ]
  },
  "sans": {
    "name": "Small-Angle Neutron Scattering",
    "description": "BIO-SANS, EQ-SANS, GP-SANS, USANS",
    "icon": "mdi-atom",
    "theme": "NeutronsTheme",
    "tools": [
      {
        "id": "neutrons_trame_sans",
        "name": "SANS Data Reduction",
        "description": "Small-Angle Neutron Scattering Data Reduction Application",
        "max_instances": 1
      }
    ]
  },
  "direct-geometry-spectroscopy": {
    "name": "Direct-Geometry Spectroscopy",
    "description": "ARCS, CNCS, CTAX, HYSPEC, NSE, PTAX, SEQUOIA, TAX, VERITAS",
    "icon": "mdi-microscope",
    "theme": "NeutronsTheme",
    "tools": []
  },
  "chemical-spectroscopy": {
    "name": "Chemical Spectroscopy",
    "description": "BASIS, VISION",
    "icon": "mdi-microscope",
    "theme": "NeutronsTheme",
    "tools": []
  },
  "imaging": {
    "name": "Imaging",
    "description": "MARS, VENUS",
    "icon": "mdi-chart-bell-curve-cumulative",
    "theme": "NeutronsTheme",
    "tools": [
      {
        "id": "neutrons_ctr",
        "name": "CT Reconstruction",
        "description": "Computed Tomography Reconstruction in a Jupyter Notebook",
        "max_instances": 1
      }
    ]
  },
  "tools": {
    "name": "Miscellaneous",
    "description": "Jupyter Notebook, Paraview",
    "icon": "mdi-tools",
    "theme": "NeutronsTheme",
    "tools": [
      {
        "id": "interactive_tool_generic_output",
        "name": "Jupyter Notebook",
        "description": "Run a Jupyter Notebook",
        "max_instances": 1
      },
      {
        "id": "interactive_tool_paraview",
        "name": "Paraview",
        "description": "Paraview Server for Scientific Visualization",
        "max_instances": 1
      },
      {
        "id": "interactive_tool_amira",
        "name": "Amira",
        "description": "Amira Visualizer",
        "max_instances": 1
      },
      {
        "id": "interactive_tool_jana2020",
        "name": "Jana2020",
        "description": "Jana2020 Visualizer",
        "max_instances": 1
      },
      {
        "id": "interactive_tool_sasview",
        "name": "SASView",
        "description": "SASView",
        "max_instances": 1
      }
    ]
  }
}
"""
class ToolModel:

    def __init__(self):
        # self.tools = json.load(open(TOOL_PATH, "r"))
        self.tools = json.loads(json_string)
    def get_tools(self, as_list=False):
        if as_list:
            return [
                tool
                for category in self.tools.values()
                for tool in category.get("tools", [])
            ]
        return self.tools
