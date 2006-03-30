/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 14-Jan-04  Bob Ippolito <bob@redivi.com>
 *      added cr2-cr4 to the registers to be saved.
 *      Open questions: Should we save FP registers?
 *      What about vector registers?
 *      Differences between darwin and unix?
 * 24-Nov-02  Christian Tismer  <tismer@tismer.com>
 *      needed to add another magic constant to insure
 *      that f in slp_eval_frame(PyFrameObject *f)
 *      gets included into the saved stack area.
 *      STACK_REFPLUS will probably be 1 in most cases.
 * 17-Sep-02  Christian Tismer  <tismer@tismer.com>
 *      after virtualizing stack save/restore, the
 *      stack size shrunk a bit. Needed to introduce
 *      an adjustment STACK_MAGIC per platform.
 * 15-Sep-02  Gerd Woetzel       <gerd.woetzel@GMD.DE>
 *      slightly changed framework for sparc
 * 29-Jun-02  Christian Tismer  <tismer@tismer.com>
 *      Added register 13-29, 31 saves. The same way as
 *      Armin Rigo did for the x86_unix version.
 *      This seems to be now fully functional!
 * 04-Mar-02  Hye-Shik Chang  <perky@fallin.lv>
 *      Ported from i386.
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL

#define STACK_MAGIC 3

#define REGS_TO_SAVE "r13", "r14", "r15", "r16", "r17", "r18", "r19", "r20", \
       "r21", "r22", "r23", "r24", "r25", "r26", "r27", "r28", "r29", "r31", \
       "cr2", "cr3", "cr4"
static int
slp_switch(void)
{
    register int *stackref, stsizediff;
    __asm__ volatile ("" : : : REGS_TO_SAVE);
    __asm__ ("mr %0, r1" : "=g" (stackref) : );
    {
        SLP_SAVE_STATE(stackref, stsizediff);
        __asm__ volatile (
            "mr r11, %0\n"
            "add r1, r1, r11\n"
            "add r30, r30, r11\n"
            : /* no outputs */
            : "g" (stsizediff)
            : "r11"
            );
        SLP_RESTORE_STATE();
        return 0;
    }
    __asm__ volatile ("" : : : REGS_TO_SAVE);
}

#endif

/*
 * further self-processing support
 */

/* 
 * if you want to add self-inspection tools, place them
 * here. See the x86_msvc for the necessary defines.
 * These features are highly experimental und not
 * essential yet.
 */
