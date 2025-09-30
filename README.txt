Voxel is innovative language based on brainfuck-like instructions with high-level features like pyl and assembly-like syntax.
Example:
```
:voxel-setup-{
    @start /:
    @include= tape /:
    @include= first_program /:
    //= Your_setup-voxel_here /:
};

:voxel-program-{
    pyl= main('User') /:
    //= Your_program-voxel_here /:
};

= Start;

:voxel-main-{
    use= setup /:
    use= program /:
    //= Your_main-voxel_here /:
};

use= main;
= End;
```
- that is basic structure of voxel programm.
