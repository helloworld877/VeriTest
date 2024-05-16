module encoder31 (input [1:0] in, output reg [1:0] out);

    always @* begin
        case(in)
            2'b01: out = 2'b01;
            2'b10: out = 2'b10;
            default: out = 2'b00; // Handle undefined case
        endcase
    end

endmodule
