#include <memory> // for unique_ptr

#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"

class CustomSource : public openmc::Source
{
  openmc::SourceSite sample(uint64_t* seed) const
  {
    openmc::SourceSite particle;
    // weight
    particle.particle = openmc::ParticleType::neutron;
    particle.wgt = 1.0;
    // position
    float R = 1;
    float gamma = openmc::prn(seed);
    float alpha = openmc::prn(seed);
    float angle = 2 * M_PI * gamma;
    float radius = R * std::sqrt(alpha);
    particle.r.x = radius * std::cos(angle);
    particle.r.y = radius * std::sin(angle);
    particle.r.z = 0.0;
    // angle
    particle.u = {0.0,0.0,1.0};
    particle.E = 30.0;
    particle.delayed_group = 0;
    return particle;
  }
};

extern "C" std::unique_ptr<CustomSource> openmc_create_source(std::string parameters)
{
  return std::make_unique<CustomSource>();
}
