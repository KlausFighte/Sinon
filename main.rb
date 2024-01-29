#require 'google/cloud/speech'
#require 'ruby-audio'

#def read_audio_data_from_microphone
  #input = AudioInput.new

  #buffer_size = 1024
  #buffer = []

  #input.each_buffer(buffer_size) do |data|
    #buffer << data
  #  next if buffer.size < buffer_size

    #audio_data = buffer.flatten.pack('s*')
#
#    buffer.clear
#
#    return audio_data
#  end
#end
#
#class AudioInput
#  def initialize
#    @input = RubyAudio::Sound.new(
#      channels: 1,
#      format: RubyAudio::FORMAT_PCM_16,
#      rate: 16000
#    )
#    @input.start
#  end
##
#  def each_buffer(buffer_size)
  #  buffer = RubyAudio::Buffer.float(buffer_size)
  #  loop do
  #    read_size = @input.read(buffer)
  #    yield buffer.to_a[0, read_size]
  #  end
#  end
#end


#def streaming_recognize
#  speech_client = Google::Cloud::Speech.speech

#  config = {
#    encoding:          :LINEAR16,
#    sample_rate_hertz: 16_000,
#    language_code:     "en-US",
#  }

#  streaming_config = {
#    config:    config,
#    interim_results: true,
#  }

#  audio_stream = speech_client.streaming_recognize(streaming_config)

#  begin
#    puts "Голосовой ассистент готов к работе. Говорите что-нибудь..."
#
#    loop do

#      audio_data = read_audio_data_from_microphone

#      break if audio_data.nil?
#      audio_stream.send audio_data
#      results = audio_stream.recognize


#      results.each do |result|
#        puts "Распознано: #{result.transcript}" if result.is_final?
#      end
#    end
##  ensure
  #  audio_stream.stop
#  end
#end

#streaming_recognize
#//by.klaus
