#include <proto/exec.h>
#include <proto/dos.h>
#include <proto/uae.h>
#include <dos/dos.h>

#include <resources/uae.h>
#include "uae_emulib.h"

static const char *TEMPLATE =
   "QUIET/S,"
   "KILL/S";
typedef struct {
  ULONG *quiet;
  ULONG *kill;
} params_t;


int main(void)
{
  struct RDArgs *args;
  struct UAEResource *UAEBase;
  params_t params = { NULL, NULL };

  /* get uae.resource */
  UAEBase = OpenResource(UAENAME);
  if(UAEBase == NULL) {
    PutStr("ERROR: No uae.resource found!\n");
    return RETURN_ERROR;
  }

  /* First parse args */
  args = ReadArgs(TEMPLATE, (LONG *)&params, NULL);
  if(args == NULL) {
    PrintFault(IoErr(), "Args Error");
    return RETURN_ERROR;
  }

  /* print version */
  if(!params.quiet) {
    Printf("UAE %ld.%ld.%ld  ROM=@%08lx\n",
      (ULONG)UAEBase->uae_version, (ULONG)UAEBase->uae_revision,
      (ULONG)UAEBase->uae_subrevision, UAEBase->uae_rombase);
  }

  /* get uaelib_demux func */
  APTR uaelib_demux = UAEGetFunc("uaelib_demux");
  int result;
  if(uaelib_demux != NULL) {
    if(!params.quiet) {
      Printf("demux=%08lx\n", uaelib_demux);
    }
    uae_lib_call uae_lib = (uae_lib_call)uaelib_demux;

    /* test version call */
    if(!params.quiet) {
      ULONG ver = uae_lib(UAE_EMULIB_GET_VERSION);
      Printf("version=%08lx\n", ver);
    }

    /* kill emu? */
    if(params.kill) {
      if(!params.quiet) {
        Printf("killing emu!\n");
      }
      uae_lib(UAE_EMULIB_EXIT_EMU);
    }

    result = RETURN_OK;
  } else {
    PutStr("ERROR: No 'uaelib_demux' trap found!\n");
    result = RETURN_ERROR;
  }

  /* Finally free args */
  FreeArgs(args);
  return result;
}
