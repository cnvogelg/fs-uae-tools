#ifndef RESOURCES_UAE_H
#define RESOURCES_UAE_H

/*
** The UAE Resource
*/

#ifndef EXEC_TYPES_H
#include <exec/types.h>
#endif

#ifndef EXEC_LIBRARIES_H
#include <exec/libraries.h>
#endif

struct UAEResource {
  struct Library  uae_Library;
  UWORD           uae_version;
  UWORD           uae_revision;
  UWORD           uae_subrevision;
  UWORD           zero;
  APTR            uae_rombase;
};

#define UAENAME    "uae.resource"

#endif /* RESOURCES_UAE_H */
