# Computer_Networking
The work practice from Computer Networking in Python

PA1–A: Basic Proxy
For the first part of the assignment, the focus will be on basic (single client) proxy functionality. Specifically, we will evaluate your code by performing tests similar to those described in part PA1-A.

What to hand in.
Submit your completed sub-assignment via Gradescope using the button link at the bottom of this page by the due date. Your submission should consist of a single Python source file named HTTPproxy.py. If you want to share information about your submission with the TAs, put that information in comments at the top of your Python source file.

PA1–B: Multi-client Proxy
For this part of the assignment, you are to develop the multi-client proxy as described in part PA1-B. At this point, the emphasis will be on the multi-client aspect of the proxy. We will evaluate your code by performing tests similar to those described in part PA1-B. (Of course, the basic proxy functionality should continue to work, too!)

What to hand in.
Submit your completed sub-assignment via Gradescope using the button link on assignment PA1-B by the due date. Your submission should consist of a single Python source file named HTTPproxy.py. If you want to share information about your submission with the TAs, put that information in comments at the top of your Python source file.

PA1–Final: Complete Assignment
For your final submission, you should implement the remaining required functionality in your proxy. Your final submission will be tested more thoroughly, using tests like those described in all parts (PA1-A, PA1-B, and PA1-Final). The TAs will also inspect your code for general quality and robustness, including inline documentation.

PA2
A real transport protocol would typically be implemented in the kernel of an operating system. To simplify your development, your code will execute in a simulated hardware/software environment. However, the programming interface provided to your code—i.e., the code that would call your entities from above and from below—is similar to what is done in an actual UNIX operating system. Stopping/starting of timers are also simulated, and timer interrupts will cause your timer-handling routine to be activated.

PA3
implement a Go-Back-N, unidirectional, reliable transfer of data from the A-side to the B-side, with a window size equal to 1/2 of the simulation’s seqnum_limit value. The value of seqnum_limit is passed to EntityA.__init__() and to EntityB.__init__() when the simulation starts.
