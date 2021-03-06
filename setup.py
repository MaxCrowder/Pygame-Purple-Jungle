import cx_Freeze

executables = [cx_Freeze.Executable("app.py")]

cx_Freeze.setup(
    name="Purple Jungle",
    options={
        "build_exe": {"packages": ["pygame", "sys"],
                      "include_files": ["map.txt",
                                        "assets/background1.png",
                                        "assets/background2.png",
                                        "assets/background3.png",
                                        "assets/background4.png",
                                        "assets/top.png",
                                        "assets/bottom.png",
                                        "animations/idle/idle_0.png",
                                        "animations/idle/idle_1.png",
                                        "animations/idle/idle_2.png",
                                        "animations/idle/idle_3.png",
                                        "animations/idle/idle_4.png",
                                        "animations/idle/idle_5.png",
                                        "animations/idle/idle_6.png",
                                        "animations/idle/idle_7.png",
                                        "animations/run/run_0.png",
                                        "animations/run/run_1.png",
                                        "animations/run/run_2.png",
                                        "animations/run/run_3.png",
                                        "animations/run/run_4.png",
                                        "animations/run/run_5.png",
                                        "animations/run/run_6.png",
                                        "animations/run/run_7.png",
                                        "animations/jump/jump_0.png",
                                        "animations/jump/jump_1.png",
                                        "animations/jump/jump_2.png",
                                        "animations/jump/jump_3.png",
                                        "animations/jump/jump_4.png",
                                        "animations/jump/jump_5.png",
                                        "animations/jump/jump_6.png",
                                        "animations/jump/jump_7.png",
                                         ]}}, executables=executables)
