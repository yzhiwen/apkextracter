
-keep class com.yangzhiwen.sample.W { *; }

# -keep class com.yangzhiwen.sample.Hello { *; }
# -keep class com.yangzhiwen.sample.Hello {
#    !private <fields>;
#    !private <methods>;
# }
# -keep class com.yangzhiwen.sample.Hello

# -keep class com.yangzhiwen.sample.* # 混淆匹配类的内部实现，不混淆类名
-keep class com.yangzhiwen.** # 混淆匹配类的内部实现，不混淆类名