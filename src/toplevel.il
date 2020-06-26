attribute \generator "nMigen"
attribute \nmigen.hierarchy "top.dut"
module \dut
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 input 0 \clk
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 input 1 \rd_en
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 output 2 \empty
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 \empty$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 input 3 \wr_en
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 output 4 \full
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 \full$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
  wire width 1 input 5 \rst
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 8 output 6 \rd_data
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 8 \rd_data$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 8 input 7 \wr_data
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ir.py:526"
  wire width 1 input 8 \rst$1
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ir.py:526"
  wire width 1 input 9 \clk$2
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/misc_util.py:43"
  wire width 1 \dom_clk
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/misc_util.py:43"
  wire width 1 \dom_rst
  process $group_0
    assign \dom_clk 1'0
    assign \dom_clk \clk
    sync init
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:102"
  wire width 8 \last_rd_val
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:102"
  wire width 8 \last_rd_val$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:213"
  wire width 2 \rd
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:213"
  wire width 2 \rd$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:78"
  wire width 8 $signal
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:78"
  wire width 8 $signal$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:78"
  wire width 8 $signal$3
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:78"
  wire width 8 $signal$3$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:78"
  wire width 8 $signal$4
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:78"
  wire width 8 $signal$4$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:78"
  wire width 8 $signal$5
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:78"
  wire width 8 $signal$5$next
  process $group_1
    assign \last_rd_val$next \last_rd_val
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:113"
    switch \rd
      case 2'00
        assign \last_rd_val$next $signal
      case 2'01
        assign \last_rd_val$next $signal$3
      case 2'10
        assign \last_rd_val$next $signal$4
      case 2'--
        assign \last_rd_val$next $signal$5
    end
    attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/xfrm.py:530"
    switch \dom_rst
      case 1'1
        assign \last_rd_val$next 8'00000000
    end
    sync init
      update \last_rd_val 8'00000000
    sync posedge \dom_clk
      update \last_rd_val \last_rd_val$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:106"
  wire width 8 \wd_cnt
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:106"
  wire width 8 \wd_cnt$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:114"
  wire width 9 $6
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:114"
  wire width 9 $7
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:114"
  cell $sub $8
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 4'1000
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 3'101
    parameter \Y_WIDTH 4'1001
    connect \A \wd_cnt
    connect \B 5'10000
    connect \Y $7
  end
  connect $6 $7
  process $group_2
    assign \wd_cnt$next \wd_cnt
    assign \wd_cnt$next $6 [7:0]
    attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/xfrm.py:530"
    switch \dom_rst
      case 1'1
        assign \wd_cnt$next 8'10100000
    end
    sync init
      update \wd_cnt 8'10100000
    sync posedge \dom_clk
      update \wd_cnt \wd_cnt$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:103"
  wire width 2 \test_wr
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  wire width 3 $9
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:83"
  wire width 2 \wr
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:83"
  wire width 2 \wr$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  wire width 3 $10
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  cell $add $11
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 2'11
    connect \A \wr
    connect \B 1'1
    connect \Y $10
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  wire width 3 $12
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  cell $mod $13
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'11
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'11
    parameter \Y_WIDTH 2'11
    connect \A $10
    connect \B 3'100
    connect \Y $12
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  wire width 3 $14
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  wire width 3 $15
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  cell $add $16
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 2'11
    connect \A \wr
    connect \B 1'1
    connect \Y $15
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/back/rtlil.py:525"
  wire width 1 $17
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/back/rtlil.py:525"
  cell $eq $18
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'11
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $15
    connect \B 1'0
    connect \Y $17
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:118"
  cell $mux $19
    parameter \WIDTH 2'11
    connect \A $12
    connect \B 3'000
    connect \S $17
    connect \Y $14
  end
  connect $9 $14
  process $group_3
    assign \test_wr 2'00
    assign \test_wr $9 [1:0]
    sync init
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:88"
  wire width 2 \incr_rd
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:127"
  wire width 3 $20
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:128"
  wire width 3 $21
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:128"
  cell $add $22
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 2'11
    connect \A \rd
    connect \B 1'1
    connect \Y $21
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:127"
  wire width 3 $23
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:85"
  wire width 3 $24
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:85"
  cell $add $25
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 2'11
    connect \A \rd
    connect \B 1'1
    connect \Y $24
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:127"
  wire width 1 $26
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:127"
  cell $lt $27
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'11
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'11
    parameter \Y_WIDTH 1'1
    connect \A $24
    connect \B 3'100
    connect \Y $26
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:127"
  cell $mux $28
    parameter \WIDTH 2'11
    connect \A 3'000
    connect \B $21
    connect \S $26
    connect \Y $23
  end
  connect $20 $23
  process $group_4
    assign \incr_rd 2'00
    assign \incr_rd $20 [1:0]
    sync init
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:89"
  wire width 2 \incr_wr
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:129"
  wire width 3 $29
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:130"
  wire width 3 $30
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:130"
  cell $add $31
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 2'11
    connect \A \wr
    connect \B 1'1
    connect \Y $30
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:129"
  wire width 3 $32
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:86"
  wire width 3 $33
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:86"
  cell $add $34
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 2'11
    connect \A \wr
    connect \B 1'1
    connect \Y $33
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:129"
  wire width 1 $35
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:129"
  cell $lt $36
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'11
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'11
    parameter \Y_WIDTH 1'1
    connect \A $33
    connect \B 3'100
    connect \Y $35
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:129"
  cell $mux $37
    parameter \WIDTH 2'11
    connect \A 3'000
    connect \B $30
    connect \S $35
    connect \Y $32
  end
  connect $29 $32
  process $group_5
    assign \incr_wr 2'00
    assign \incr_wr $29 [1:0]
    sync init
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:91"
  wire width 1 \next_empty
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:95"
  wire width 2 \next_wr
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:94"
  wire width 2 \next_rd
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:132"
  wire width 1 $38
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:132"
  cell $eq $39
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A \next_wr
    connect \B \next_rd
    connect \Y $38
  end
  process $group_6
    assign \next_empty 1'0
    assign \next_empty $38
    sync init
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:138"
  wire width 1 $40
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:138"
  cell $not $41
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \empty
    connect \Y $40
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:138"
  wire width 1 $42
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:138"
  cell $and $43
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rd_en
    connect \B $40
    connect \Y $42
  end
  process $group_7
    assign \next_rd 2'00
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:138"
    switch { $42 }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:138"
      case 1'1
        assign \next_rd \incr_rd
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:140"
      case
        assign \next_rd \rd
    end
    sync init
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
  wire width 1 $44
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
  cell $not $45
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \full
    connect \Y $44
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
  wire width 1 $46
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
  cell $and $47
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \wr_en
    connect \B $44
    connect \Y $46
  end
  process $group_8
    assign \next_wr 2'00
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
    switch { $46 }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
      case 1'1
        assign \next_wr \incr_wr
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:149"
      case
        assign \next_wr \wr
    end
    sync init
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:92"
  wire width 1 \next_full
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
  wire width 1 $48
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
  cell $not $49
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \full
    connect \Y $48
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
  wire width 1 $50
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
  cell $and $51
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \wr_en
    connect \B $48
    connect \Y $50
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:147"
  wire width 3 $52
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:147"
  cell $add $53
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 2'11
    connect \A \incr_wr
    connect \B 1'1
    connect \Y $52
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:147"
  wire width 1 $54
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:147"
  cell $eq $55
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'11
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A $52
    connect \B \next_rd
    connect \Y $54
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:153"
  wire width 1 $56
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:153"
  cell $eq $57
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A \incr_wr
    connect \B \next_rd
    connect \Y $56
  end
  process $group_9
    assign \next_full 1'0
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
    switch { $50 }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:143"
      case 1'1
        assign \next_full $54
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:149"
      case
        assign \next_full $56
    end
    sync init
  end
  process $group_10
    assign \rd$next \rd
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
        assign \rd$next 2'00
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        assign \rd$next \next_rd
    end
    attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/xfrm.py:530"
    switch \dom_rst
      case 1'1
        assign \rd$next 2'00
    end
    sync init
      update \rd 2'00
    sync posedge \dom_clk
      update \rd \rd$next
  end
  process $group_11
    assign \wr$next \wr
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
        assign \wr$next 2'00
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        assign \wr$next \next_wr
    end
    attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/xfrm.py:530"
    switch \dom_rst
      case 1'1
        assign \wr$next 2'00
    end
    sync init
      update \wr 2'00
    sync posedge \dom_clk
      update \wr \wr$next
  end
  process $group_12
    assign \empty$next \empty
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
        assign \empty$next 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        assign \empty$next \next_empty
    end
    attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/xfrm.py:530"
    switch \dom_rst
      case 1'1
        assign \empty$next 1'0
    end
    sync init
      update \empty 1'0
    sync posedge \dom_clk
      update \empty \empty$next
  end
  process $group_13
    assign \full$next \full
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
        assign \full$next 1'0
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        assign \full$next \next_full
    end
    attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/xfrm.py:530"
    switch \dom_rst
      case 1'1
        assign \full$next 1'0
    end
    sync init
      update \full 1'0
    sync posedge \dom_clk
      update \full \full$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:183"
  wire width 1 $58
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:183"
  cell $not $59
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \empty
    connect \Y $58
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:183"
  wire width 1 $60
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:183"
  cell $and $61
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rd_en
    connect \B $58
    connect \Y $60
  end
  process $group_14
    assign \rd_data$next \rd_data
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:183"
        switch { $60 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:183"
          case 1'1
            attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:184"
            switch \rd
              case 2'00
                assign \rd_data$next $signal
              case 2'01
                assign \rd_data$next $signal$3
              case 2'10
                assign \rd_data$next $signal$4
              case 2'--
                assign \rd_data$next $signal$5
            end
        end
    end
    attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/xfrm.py:530"
    switch \dom_rst
      case 1'1
        assign \rd_data$next 8'00000000
    end
    sync init
      update \rd_data 8'00000000
    sync posedge \dom_clk
      update \rd_data \rd_data$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:185"
  wire width 1 $62
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:185"
  cell $not $63
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \full
    connect \Y $62
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:185"
  wire width 1 $64
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:185"
  cell $and $65
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \wr_en
    connect \B $62
    connect \Y $64
  end
  process $group_15
    assign $signal$next $signal
    assign $signal$3$next $signal$3
    assign $signal$4$next $signal$4
    assign $signal$5$next $signal$5
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:185"
        switch { $64 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:185"
          case 1'1
            attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:186"
            switch \wr
              case 2'00
                assign $signal$next \wr_data
              case 2'01
                assign $signal$3$next \wr_data
              case 2'10
                assign $signal$4$next \wr_data
              case 2'--
                assign $signal$5$next \wr_data
            end
        end
    end
    attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/xfrm.py:530"
    switch \dom_rst
      case 1'1
        assign $signal$next 8'00000000
        assign $signal$3$next 8'00000000
        assign $signal$4$next 8'00000000
        assign $signal$5$next 8'00000000
    end
    sync init
      update $signal 8'00000000
      update $signal$3 8'00000000
      update $signal$4 8'00000000
      update $signal$5 8'00000000
    sync posedge \dom_clk
      update $signal $signal$next
      update $signal$3 $signal$3$next
      update $signal$4 $signal$4$next
      update $signal$5 $signal$5$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:194"
  wire width 1 $assert$en
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:194"
  wire width 1 $assert$en$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:194"
  wire width 1 $assert$check
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:194"
  wire width 1 $assert$check$next
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
  wire width 1 $sample$s$rst$sync$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
  wire width 1 $sample$s$rst$sync$1$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $66
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $67
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $66
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $68
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $69
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $66
    connect \Y $68
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:194"
  wire width 1 $70
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:194"
  cell $eq $71
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rd
    connect \B 1'0
    connect \Y $70
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:194"
  cell $assert $72
    connect \A $assert$check
    connect \EN $assert$en
  end
  process $group_19
    assign $assert$en$next $assert$en
    assign $assert$check$next $assert$check
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $68 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
            assign $assert$check$next $70
            assign $assert$en$next 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
        end
    end
    sync init
      update $assert$en 1'0
      update $assert$check 1'0
    sync posedge \dom_clk
      update $assert$en $assert$en$next
      update $assert$check $assert$check$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:195"
  wire width 1 $assert$en$73
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:195"
  wire width 1 $assert$en$73$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:195"
  wire width 1 $assert$check$74
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:195"
  wire width 1 $assert$check$74$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $75
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $76
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $75
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $77
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $78
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $75
    connect \Y $77
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:195"
  wire width 1 $79
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:195"
  cell $eq $80
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \wr
    connect \B 1'0
    connect \Y $79
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:195"
  cell $assert $81
    connect \A $assert$check$74
    connect \EN $assert$en$73
  end
  process $group_21
    assign $assert$en$73$next $assert$en$73
    assign $assert$check$74$next $assert$check$74
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $77 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
            assign $assert$check$74$next $79
            assign $assert$en$73$next 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
        end
    end
    sync init
      update $assert$en$73 1'0
      update $assert$check$74 1'0
    sync posedge \dom_clk
      update $assert$en$73 $assert$en$73$next
      update $assert$check$74 $assert$check$74$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:197"
  wire width 1 $assert$en$82
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:197"
  wire width 1 $assert$en$82$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:197"
  wire width 1 $assert$check$83
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:197"
  wire width 1 $assert$check$83$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $84
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $85
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $84
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $86
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $87
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $84
    connect \Y $86
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:197"
  wire width 1 $88
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:197"
  cell $eq $89
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \empty
    connect \B 1'1
    connect \Y $88
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:197"
  cell $assert $90
    connect \A $assert$check$83
    connect \EN $assert$en$82
  end
  process $group_23
    assign $assert$en$82$next $assert$en$82
    assign $assert$check$83$next $assert$check$83
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $86 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
            assign $assert$check$83$next $88
            assign $assert$en$82$next 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
        end
    end
    sync init
      update $assert$en$82 1'0
      update $assert$check$83 1'0
    sync posedge \dom_clk
      update $assert$en$82 $assert$en$82$next
      update $assert$check$83 $assert$check$83$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:198"
  wire width 1 $assert$en$91
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:198"
  wire width 1 $assert$en$91$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:198"
  wire width 1 $assert$check$92
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:198"
  wire width 1 $assert$check$92$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $93
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $94
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $93
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $95
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $96
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $93
    connect \Y $95
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:198"
  wire width 1 $97
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:198"
  cell $eq $98
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \full
    connect \B 1'0
    connect \Y $97
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:198"
  cell $assert $99
    connect \A $assert$check$92
    connect \EN $assert$en$91
  end
  process $group_25
    assign $assert$en$91$next $assert$en$91
    assign $assert$check$92$next $assert$check$92
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $95 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
            assign $assert$check$92$next $97
            assign $assert$en$91$next 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
        end
    end
    sync init
      update $assert$en$91 1'0
      update $assert$check$92 1'0
    sync posedge \dom_clk
      update $assert$en$91 $assert$en$91$next
      update $assert$check$92 $assert$check$92$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  wire width 1 $assert$en$100
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  wire width 1 $assert$en$100$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  wire width 1 $assert$check$101
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  wire width 1 $assert$check$101$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $102
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $103
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $102
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $104
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $105
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $102
    connect \Y $104
  end
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  wire width 1 $sample$s$next_empty$dom$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  wire width 1 $sample$s$next_empty$dom$1$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  wire width 1 $106
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  cell $eq $107
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \empty
    connect \B $sample$s$next_empty$dom$1
    connect \Y $106
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:203"
  cell $assert $108
    connect \A $assert$check$101
    connect \EN $assert$en$100
  end
  process $group_27
    assign $assert$en$100$next $assert$en$100
    assign $assert$check$101$next $assert$check$101
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $104 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            assign $assert$check$101$next $106
            assign $assert$en$100$next 1'1
        end
    end
    sync init
      update $assert$en$100 1'0
      update $assert$check$101 1'0
    sync posedge \dom_clk
      update $assert$en$100 $assert$en$100$next
      update $assert$check$101 $assert$check$101$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  wire width 1 $assert$en$109
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  wire width 1 $assert$en$109$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  wire width 1 $assert$check$110
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  wire width 1 $assert$check$110$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $111
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $112
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $111
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $113
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $114
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $111
    connect \Y $113
  end
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  wire width 1 $sample$s$next_full$dom$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  wire width 1 $sample$s$next_full$dom$1$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  wire width 1 $115
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  cell $eq $116
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \full
    connect \B $sample$s$next_full$dom$1
    connect \Y $115
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:204"
  cell $assert $117
    connect \A $assert$check$110
    connect \EN $assert$en$109
  end
  process $group_29
    assign $assert$en$109$next $assert$en$109
    assign $assert$check$110$next $assert$check$110
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $113 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            assign $assert$check$110$next $115
            assign $assert$en$109$next 1'1
        end
    end
    sync init
      update $assert$en$109 1'0
      update $assert$check$110 1'0
    sync posedge \dom_clk
      update $assert$en$109 $assert$en$109$next
      update $assert$check$110 $assert$check$110$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  wire width 1 $assert$en$118
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  wire width 1 $assert$en$118$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  wire width 1 $assert$check$119
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  wire width 1 $assert$check$119$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $120
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $121
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $120
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $122
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $123
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $120
    connect \Y $122
  end
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  wire width 2 $sample$s$next_rd$dom$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  wire width 2 $sample$s$next_rd$dom$1$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  wire width 1 $124
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  cell $eq $125
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A \rd
    connect \B $sample$s$next_rd$dom$1
    connect \Y $124
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:205"
  cell $assert $126
    connect \A $assert$check$119
    connect \EN $assert$en$118
  end
  process $group_31
    assign $assert$en$118$next $assert$en$118
    assign $assert$check$119$next $assert$check$119
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $122 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            assign $assert$check$119$next $124
            assign $assert$en$118$next 1'1
        end
    end
    sync init
      update $assert$en$118 1'0
      update $assert$check$119 1'0
    sync posedge \dom_clk
      update $assert$en$118 $assert$en$118$next
      update $assert$check$119 $assert$check$119$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  wire width 1 $assert$en$127
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  wire width 1 $assert$en$127$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  wire width 1 $assert$check$128
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  wire width 1 $assert$check$128$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $129
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $130
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $129
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $131
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $132
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $129
    connect \Y $131
  end
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  wire width 2 $sample$s$next_wr$dom$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  wire width 2 $sample$s$next_wr$dom$1$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  wire width 1 $133
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  cell $eq $134
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A \wr
    connect \B $sample$s$next_wr$dom$1
    connect \Y $133
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:206"
  cell $assert $135
    connect \A $assert$check$128
    connect \EN $assert$en$127
  end
  process $group_33
    assign $assert$en$127$next $assert$en$127
    assign $assert$check$128$next $assert$check$128
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $131 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            assign $assert$check$128$next $133
            assign $assert$en$127$next 1'1
        end
    end
    sync init
      update $assert$en$127 1'0
      update $assert$check$128 1'0
    sync posedge \dom_clk
      update $assert$en$127 $assert$en$127$next
      update $assert$check$128 $assert$check$128$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:213"
  wire width 1 $assert$en$136
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:213"
  wire width 1 $assert$en$136$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:213"
  wire width 1 $assert$check$137
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:213"
  wire width 1 $assert$check$137$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $138
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $139
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $138
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $140
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $141
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $138
    connect \Y $140
  end
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:208"
  wire width 1 $sample$s$rd_en$sync$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:208"
  wire width 1 $sample$s$rd_en$sync$1$next
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:209"
  wire width 1 $sample$s$empty$sync$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:209"
  wire width 1 $sample$s$empty$sync$1$next
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:225"
  wire width 2 $sample$s$rd$dom$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:225"
  wire width 2 $sample$s$rd$dom$1$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1192"
  wire width 1 $142
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1192"
  cell $eq $143
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rd$dom$1
    connect \B \rd
    connect \Y $142
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:213"
  cell $assert $144
    connect \A $assert$check$137
    connect \EN $assert$en$136
  end
  process $group_35
    assign $assert$en$136$next $assert$en$136
    assign $assert$check$137$next $assert$check$137
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $140 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:208"
            switch { $sample$s$rd_en$sync$1 }
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:208"
              case 1'1
                attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:209"
                switch { $sample$s$empty$sync$1 }
                  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:209"
                  case 1'1
                    assign $assert$check$137$next $142
                    assign $assert$en$136$next 1'1
                  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:220"
                  case
                end
            end
        end
    end
    sync init
      update $assert$en$136 1'0
      update $assert$check$137 1'0
    sync posedge \dom_clk
      update $assert$en$136 $assert$en$136$next
      update $assert$check$137 $assert$check$137$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  wire width 1 $assert$en$145
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  wire width 1 $assert$en$145$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  wire width 1 $assert$check$146
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  wire width 1 $assert$check$146$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $147
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $148
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $147
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $149
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $150
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $147
    connect \Y $149
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:221"
  wire width 1 $151
  attribute \nmigen.sample_reg 1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:221"
  wire width 1 $sample$s$wr_en$sync$1
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:221"
  wire width 1 $sample$s$wr_en$sync$1$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:221"
  cell $not $152
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$wr_en$sync$1
    connect \Y $151
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  wire width 1 $153
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  cell $eq $154
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 4'1000
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 4'1000
    parameter \Y_WIDTH 1'1
    connect \A \rd_data
    connect \B $signal
    connect \Y $153
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  wire width 1 $155
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  cell $eq $156
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 4'1000
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 4'1000
    parameter \Y_WIDTH 1'1
    connect \A \rd_data
    connect \B $signal$3
    connect \Y $155
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  wire width 1 $157
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  cell $eq $158
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 4'1000
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 4'1000
    parameter \Y_WIDTH 1'1
    connect \A \rd_data
    connect \B $signal$4
    connect \Y $157
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  wire width 1 $159
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  cell $eq $160
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 4'1000
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 4'1000
    parameter \Y_WIDTH 1'1
    connect \A \rd_data
    connect \B $signal$5
    connect \Y $159
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:224"
  cell $assert $161
    connect \A $assert$check$146
    connect \EN $assert$en$145
  end
  process $group_37
    assign $assert$en$145$next $assert$en$145
    assign $assert$check$146$next $assert$check$146
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $149 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:208"
            switch { $sample$s$rd_en$sync$1 }
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:208"
              case 1'1
                attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:209"
                switch { $sample$s$empty$sync$1 }
                  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:209"
                  case 1'1
                  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:220"
                  case
                    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:221"
                    switch { $151 }
                      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:221"
                      case 1'1
                        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:225"
                        switch $sample$s$rd$dom$1
                          case 2'00
                            assign $assert$check$146$next $153
                          case 2'01
                            assign $assert$check$146$next $155
                          case 2'10
                            assign $assert$check$146$next $157
                          case 2'--
                            assign $assert$check$146$next $159
                        end
                        switch { }
                          case
                            assign $assert$en$145$next 1'1
                        end
                    end
                end
            end
        end
    end
    sync init
      update $assert$en$145 1'0
      update $assert$check$146 1'0
    sync posedge \dom_clk
      update $assert$en$145 $assert$en$145$next
      update $assert$check$146 $assert$check$146$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:231"
  wire width 1 $assume$en
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:231"
  wire width 1 $assume$en$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:231"
  wire width 1 $assume$check
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:231"
  wire width 1 $assume$check$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $162
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $163
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $162
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $164
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $165
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $162
    connect \Y $164
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:231"
  wire width 1 $166
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:231"
  cell $ne $167
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A \wr
    connect \B \rd
    connect \Y $166
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:231"
  cell $assume $168
    connect \A $assume$check
    connect \EN $assume$en
  end
  process $group_39
    assign $assume$en$next $assume$en
    assign $assume$check$next $assume$check
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $164 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:227"
            switch { \full \empty }
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:228"
              case 2'00
                assign $assume$check$next $166
                assign $assume$en$next 1'1
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:234"
              case 2'01
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:239"
              case 2'10
            end
        end
    end
    sync init
      update $assume$en 1'0
      update $assume$check 1'0
    sync posedge \dom_clk
      update $assume$en $assume$en$next
      update $assume$check $assume$check$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:232"
  wire width 1 $assume$en$169
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:232"
  wire width 1 $assume$en$169$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:232"
  wire width 1 $assume$check$170
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:232"
  wire width 1 $assume$check$170$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $171
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $172
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $171
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $173
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $174
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $171
    connect \Y $173
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:232"
  wire width 1 $175
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:232"
  cell $ne $176
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A \test_wr
    connect \B \rd
    connect \Y $175
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:232"
  cell $assume $177
    connect \A $assume$check$170
    connect \EN $assume$en$169
  end
  process $group_41
    assign $assume$en$169$next $assume$en$169
    assign $assume$check$170$next $assume$check$170
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $173 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:227"
            switch { \full \empty }
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:228"
              case 2'00
                assign $assume$check$170$next $175
                assign $assume$en$169$next 1'1
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:234"
              case 2'01
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:239"
              case 2'10
            end
        end
    end
    sync init
      update $assume$en$169 1'0
      update $assume$check$170 1'0
    sync posedge \dom_clk
      update $assume$en$169 $assume$en$169$next
      update $assume$check$170 $assume$check$170$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:237"
  wire width 1 $assert$en$178
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:237"
  wire width 1 $assert$en$178$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:237"
  wire width 1 $assert$check$179
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:237"
  wire width 1 $assert$check$179$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $180
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $181
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $180
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $182
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $183
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $180
    connect \Y $182
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:237"
  wire width 1 $184
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:237"
  cell $eq $185
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A \wr
    connect \B \rd
    connect \Y $184
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:237"
  cell $assert $186
    connect \A $assert$check$179
    connect \EN $assert$en$178
  end
  process $group_43
    assign $assert$en$178$next $assert$en$178
    assign $assert$check$179$next $assert$check$179
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $182 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:227"
            switch { \full \empty }
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:228"
              case 2'00
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:234"
              case 2'01
                assign $assert$check$179$next $184
                assign $assert$en$178$next 1'1
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:239"
              case 2'10
            end
        end
    end
    sync init
      update $assert$en$178 1'0
      update $assert$check$179 1'0
    sync posedge \dom_clk
      update $assert$en$178 $assert$en$178$next
      update $assert$check$179 $assert$check$179$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:242"
  wire width 1 $assert$en$187
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:242"
  wire width 1 $assert$en$187$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:242"
  wire width 1 $assert$check$188
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:242"
  wire width 1 $assert$check$188$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $189
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $190
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $189
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $191
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $192
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $189
    connect \Y $191
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:242"
  wire width 1 $193
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:242"
  cell $eq $194
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 2'10
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 2'10
    parameter \Y_WIDTH 1'1
    connect \A \test_wr
    connect \B \rd
    connect \Y $193
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:242"
  cell $assert $195
    connect \A $assert$check$188
    connect \EN $assert$en$187
  end
  process $group_45
    assign $assert$en$187$next $assert$en$187
    assign $assert$check$188$next $assert$check$188
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $191 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:227"
            switch { \full \empty }
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:228"
              case 2'00
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:234"
              case 2'01
              attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:239"
              case 2'10
                assign $assert$check$188$next $193
                assign $assert$en$187$next 1'1
            end
        end
    end
    sync init
      update $assert$en$187 1'0
      update $assert$check$188 1'0
    sync posedge \dom_clk
      update $assert$en$187 $assert$en$187$next
      update $assert$check$188 $assert$check$188$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  wire width 1 $assert$en$196
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  wire width 1 $assert$en$196$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  wire width 1 $assert$check$197
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  wire width 1 $assert$check$197$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $198
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $199
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $198
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $200
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $201
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $198
    connect \Y $200
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  wire width 1 $202
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  wire width 1 $203
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  cell $and $204
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \empty
    connect \B \full
    connect \Y $203
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  cell $not $205
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $203
    connect \Y $202
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:246"
  cell $assert $206
    connect \A $assert$check$197
    connect \EN $assert$en$196
  end
  process $group_47
    assign $assert$en$196$next $assert$en$196
    assign $assert$check$197$next $assert$check$197
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $200 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            assign $assert$check$197$next $202
            assign $assert$en$196$next 1'1
        end
    end
    sync init
      update $assert$en$196 1'0
      update $assert$check$197 1'0
    sync posedge \dom_clk
      update $assert$en$196 $assert$en$196$next
      update $assert$check$197 $assert$check$197$next
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:248"
  wire width 1 $assume$en$207
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:248"
  wire width 1 $assume$en$207$next
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:248"
  wire width 1 $assume$check$208
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:248"
  wire width 1 $assume$check$208$next
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $209
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $not $210
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A \rst
    connect \Y $209
  end
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  wire width 1 $211
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ast.py:1200"
  cell $and $212
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 1'1
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 1'1
    parameter \Y_WIDTH 1'1
    connect \A $sample$s$rst$sync$1
    connect \B $209
    connect \Y $211
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:248"
  wire width 1 $213
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:248"
  cell $eq $214
    parameter \A_SIGNED 1'0
    parameter \A_WIDTH 4'1000
    parameter \B_SIGNED 1'0
    parameter \B_WIDTH 4'1000
    parameter \Y_WIDTH 1'1
    connect \A \wr_data
    connect \B \wd_cnt
    connect \Y $213
  end
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:248"
  cell $assume $215
    connect \A $assume$check$208
    connect \EN $assume$en$207
  end
  process $group_49
    assign $assume$en$207$next $assume$en$207
    assign $assume$check$208$next $assume$check$208
    attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
    switch { \rst }
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:159"
      case 1'1
      attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:173"
      case
        attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
        switch { $211 }
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
          case 1'1
          attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:200"
          case
            assign $assume$check$208$next $213
            assign $assume$en$207$next 1'1
        end
    end
    sync init
      update $assume$en$207 1'0
      update $assume$check$208 1'0
    sync posedge \dom_clk
      update $assume$en$207 $assume$en$207$next
      update $assume$check$208 $assume$check$208$next
  end
  process $group_51
    assign $sample$s$next_empty$dom$1$next $sample$s$next_empty$dom$1
    assign $sample$s$next_empty$dom$1$next \next_empty
    sync init
      update $sample$s$next_empty$dom$1 1'0
    sync posedge \dom_clk
      update $sample$s$next_empty$dom$1 $sample$s$next_empty$dom$1$next
  end
  process $group_52
    assign $sample$s$next_full$dom$1$next $sample$s$next_full$dom$1
    assign $sample$s$next_full$dom$1$next \next_full
    sync init
      update $sample$s$next_full$dom$1 1'0
    sync posedge \dom_clk
      update $sample$s$next_full$dom$1 $sample$s$next_full$dom$1$next
  end
  process $group_53
    assign $sample$s$next_rd$dom$1$next $sample$s$next_rd$dom$1
    assign $sample$s$next_rd$dom$1$next \next_rd
    sync init
      update $sample$s$next_rd$dom$1 2'00
    sync posedge \dom_clk
      update $sample$s$next_rd$dom$1 $sample$s$next_rd$dom$1$next
  end
  process $group_54
    assign $sample$s$next_wr$dom$1$next $sample$s$next_wr$dom$1
    assign $sample$s$next_wr$dom$1$next \next_wr
    sync init
      update $sample$s$next_wr$dom$1 2'00
    sync posedge \dom_clk
      update $sample$s$next_wr$dom$1 $sample$s$next_wr$dom$1$next
  end
  process $group_55
    assign $sample$s$rd$dom$1$next $sample$s$rd$dom$1
    assign $sample$s$rd$dom$1$next \rd
    sync init
      update $sample$s$rd$dom$1 2'00
    sync posedge \dom_clk
      update $sample$s$rd$dom$1 $sample$s$rd$dom$1$next
  end
  process $group_56
    assign $sample$s$wr_en$sync$1$next $sample$s$wr_en$sync$1
    assign $sample$s$wr_en$sync$1$next \wr_en
    sync init
      update $sample$s$wr_en$sync$1 1'0
    sync posedge \clk$2
      update $sample$s$wr_en$sync$1 $sample$s$wr_en$sync$1$next
  end
  process $group_57
    assign $sample$s$empty$sync$1$next $sample$s$empty$sync$1
    assign $sample$s$empty$sync$1$next \empty
    sync init
      update $sample$s$empty$sync$1 1'0
    sync posedge \clk$2
      update $sample$s$empty$sync$1 $sample$s$empty$sync$1$next
  end
  process $group_58
    assign $sample$s$rd_en$sync$1$next $sample$s$rd_en$sync$1
    assign $sample$s$rd_en$sync$1$next \rd_en
    sync init
      update $sample$s$rd_en$sync$1 1'0
    sync posedge \clk$2
      update $sample$s$rd_en$sync$1 $sample$s$rd_en$sync$1$next
  end
  process $group_59
    assign $sample$s$rst$sync$1$next $sample$s$rst$sync$1
    assign $sample$s$rst$sync$1$next \rst
    sync init
      update $sample$s$rst$sync$1 1'0
    sync posedge \clk$2
      update $sample$s$rst$sync$1 $sample$s$rst$sync$1$next
  end
  connect \dom_rst 1'0
end
attribute \generator "nMigen"
attribute \top 1
attribute \nmigen.hierarchy "top"
module \top
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 input 0 \clk
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:191"
  wire width 1 input 1 \rst
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 input 2 \wr_en
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 8 input 3 \wr_data
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 input 4 \rd_en
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 8 output 5 \rd_data
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 output 6 \empty
  attribute \src "/media/other_data/fl4shk_home_stuff/Documents/programming_and_electronics/electronics/nmigen/small_projects_and_tests/vga_test/src/fifo_mod.py:42"
  wire width 1 output 7 \full
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ir.py:526"
  wire width 1 input 8 \clk$1
  attribute \src "/usr/lib/python3.8/site-packages/nmigen/hdl/ir.py:526"
  wire width 1 input 9 \rst$2
  cell \dut \dut
    connect \clk \clk
    connect \rd_en \rd_en
    connect \empty \empty
    connect \wr_en \wr_en
    connect \full \full
    connect \rst \rst
    connect \rd_data \rd_data
    connect \wr_data \wr_data
    connect \rst$1 \rst$2
    connect \clk$2 \clk$1
  end
end

