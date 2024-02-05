#include <memory> // for unique_ptr
#include <fstream>
#include <string>
#include <cstdlib>
#include <libxml/parser.h>
#include <stdio.h>

#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"

class CustomSource : public openmc::Source
{
public:
  CustomSource(std::string File_, std::string XML_)
  {
    File.open(File_); //, std::ios::in); // esto permite leer el archivo sin modificarlo.
    XMLfile = XML_;
    printf("Reading xmlfile %s...\n", XMLfile);
    xmlDocPtr doc = xmlReadFile(xmlfilename, NULL, 0);
    xmlNodePtr root = xmlDocGetRootElement(doc);
    xmlNodePtr node = root->children; //mcplfile
    strcpy(mpclfile, (char*)xmlNodeGetContent(node));
  }

  openmc::SourceSite sample(uint64_t *seed) const
  {
    openmc::SourceSite particle;
    // tengo que agregar algo para cerrar el archivo.
    //  weight
    particle.particle = openmc::ParticleType::neutron;
    particle.wgt = 1.0;
    // position
    std::string line;
    if (std::getline(File, line))
    {
      std::istringstream iss(line);
      iss >> particle.r.x >> particle.r.y;
    }
    else
    {
      particle.r.x = 2.0;
      particle.r.y = 2.0;
    }

    particle.r.z = 0.0;
    // angle
    particle.u = {0.0, 0.0, 1.0};
    particle.E = 30.0;
    particle.delayed_group = 0;
    return particle;
  }

private:
  mutable std::ifstream File;
  std::string XMLfile;
  std::string mpclfile;
};

extern "C" std::unique_ptr<CustomSource> openmc_create_source(std::string parameters)
{
  return std::make_unique<CustomSource>(parameters);
}
